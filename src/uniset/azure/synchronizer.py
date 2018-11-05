import logging

import requests

from . import config

logger = logging.getLogger(__name__)

USERMAP = {'_pk': ['username'],
           'username': 'userPrincipalName',
           'email': 'mail',
           'azure_id': 'id',
           'job_title': 'jobTitle',
           'display_name': 'displayName',
           'first_name': 'givenName',
           'last_name': 'surname'}


class SyncResult:
    def __init__(self, created=None, updated=None, skipped=None):
        self.created = created or []
        self.updated = updated or []
        self.skipped = skipped or []

    def log(self, result):
        if isinstance(result, (list, tuple)):
            if result[1]:
                self.created.append(result[0])
            else:
                self.updated.append(result[0])
        else:
            self.skipped.append(result)

    def __add__(self, other):
        if isinstance(other, SyncResult):
            ret = SyncResult(self.created, self.updated, self.skipped)
            ret.created.extend(other.created)
            ret.updated.extend(other.updated)
            ret.skipped.extend(other.skipped)
            return ret
        else:
            raise ValueError("Cannot add %s to SyncResult object" % type(other))

    def __repr__(self):
        return "<SyncResult: {} {} {}>".format(len(self.created),
                                               len(self.updated),
                                               len(self.skipped))

    def __eq__(self, other):
        if isinstance(other, SyncResult):
            return (self.created == other.created
                    and self.updated == other.updated
                    and self.skipped == other.skipped)
        return False


NotSet = object()


class Synchronizer:
    def __init__(self, mapping=None, echo=None, extra=None):
        self.field_map = dict(mapping or USERMAP)
        self.user_pk_fields = self.field_map.pop('_pk')
        self._baseurl = '{}/{}/users'.format(config.AZURE_GRAPH_API_BASE_URL,
                                             config.AZURE_GRAPH_API_VERSION)
        self.startUrl = "%s/delta" % self._baseurl
        self.access_token = self.get_token()
        self.next_link = None
        self._delta_link = ''
        self.echo = echo or (lambda l: True)
        self.extra = extra or {}

    def get_token(self):
        if not config.AZURE_CLIENT_ID and config.AZURE_CLIENT_SECRET:
            raise ValueError("Configure AZURE_CLIENT_ID and/or AZURE_CLIENT_SECRET")
        post_dict = {'grant_type': 'client_credentials',
                     'client_id': config.AZURE_CLIENT_ID,
                     'client_secret': config.AZURE_CLIENT_SECRET,
                     'resource': config.AZURE_GRAPH_API_BASE_URL}
        response = requests.post(config.AZURE_TOKEN_URL, post_dict)
        if response.status_code != 200:  # pragma: no cover
            logger.error("Unable to fetch token from Azure")
            raise Exception('Error during token retrieval {}'.format(response.status_code))
        jresponse = response.json()
        token = jresponse['access_token']
        return token

    @property
    def delta_link(self):
        return self._delta_link

    @delta_link.setter
    def delta_link(self, value):
        self._delta_link = value

    def get_page(self, url, single=False):
        while True:
            headers = {'Authorization': 'Bearer {}'.format(self.get_token())}
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 401:
                    data = response.json()
                    if data["error"]["message"] == "Access token has expired.":
                        continue
                    else:
                        raise ConnectionError('400: Error processing the response {}'.format(response.content))

                elif response.status_code != 200:
                    raise ConnectionError(
                        'Code {0.status_code}. Error processing the response {0.content}'.format(response))
                break
            except ConnectionError as e:
                logger.exception(e)
                raise

        jresponse = response.json()
        self.next_link = jresponse.get('@odata.nextLink', None)
        self.delta_link = jresponse.get('@odata.deltaLink', None)
        if single:
            return jresponse
        return jresponse.get('value', [])

    def __iter__(self):
        values = self.get_page(self.startUrl)
        pages = 1
        while True:
            try:
                yield values.pop()
            except IndexError:
                if not self.next_link:
                    logger.debug("All pages  fetched. deltaLink: {}".format(self.delta_link))
                    break
                values = self.get_page(self.next_link)
                logger.debug("fetched page {}".format(pages))
                pages += 1
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.exception(e)
                break

    def get_record(self, user_info):
        data = {fieldname: user_info.get(mapped_name, '')
                for fieldname, mapped_name in self.field_map.items()}
        pk = {fieldname: data.pop(fieldname) for fieldname in self.user_pk_fields}
        return pk, data

    def fetch_users(self, filter):
        self.startUrl = "%s?$filter=%s" % (self._baseurl, filter)
        return self.syncronize()

    # def sync_user(self, user):
    #     if not user.azure_id:
    #         raise ValueError("Cannot sync user without azure_id")
    #     url = "%s/%s" % (self._baseurl, user.azure_id)
    #     user_info = self.get_page(url, single=True)
    #     pk, values = self.get_record(user_info)
    #     user, __ = self.user_model.objects.update_or_create(**pk,
    #                                                         defaults=values)
    #     return user

    def resume(self, delta_link=None, max_records=None):
        if delta_link:
            self.startUrl = delta_link
        return self.syncronize(max_records)

    def is_valid(self, user_info):
        return (user_info.get('email') and user_info.get('first_name')
                and user_info.get('last_name')
                and 'noreply' not in user_info.get('email'))

    def _store(self, pk, values):
        """ :return  created """
        raise NotImplementedError

    def syncronize(self, max_records=None):
        logger.debug("Start Azure user synchronization")
        results = SyncResult()
        try:
            for i, user_info in enumerate(iter(self)):
                pk, values = self.get_record(user_info)
                if self.is_valid(values):
                    user_data = self._store(pk=pk, values=values)
                    self.echo(user_data)
                    results.log(user_data)
                else:
                    results.log(user_info)
                if max_records and i > max_records:
                    break
            else:
                results.skipped.append("")
        except Exception as e:
            logger.exception(e)
            raise
        logger.debug("End Azure user synchronization: {}".format(results))
        return results
