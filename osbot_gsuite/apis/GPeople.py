from osbot_gsuite.apis.GSuite import GSuite
from osbot_utils.decorators.methods.cache_on_tmp import cache_on_tmp
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set


class GPeople:

    def __init__(self):
        #self.api = GSuite().api('people')
        #self.api_v1 = GSuite().api('people_v1')
        pass

    def people(self):
        return GSuite().people_v1().people()

    def person(self, person_id):
        person_raw = self.person_raw(person_id)
        assert list_set(person_raw.keys()) == ['emailAddresses', 'etag', 'names', 'resourceName']
        email_addresses = person_raw.get('emailAddresses')
        names           = person_raw.get('names')
        #pprint(len(email_addresses))
        email_address   = self.primary_email_address(person_raw)
        display_name    = self.primary_display_name(person_raw)

        return {'email_address': email_address, 'display_name': display_name, 'person_id': person_id}

    def primary_display_name(self, person_raw):
        for name in person_raw.get('names'):
            if name.get('metadata').get('primary'):
                return name.get('displayName')

    def primary_email_address(self, person_raw):
        for email_address in person_raw.get('emailAddresses'):
            if email_address.get('metadata').get('primary'):
                return email_address.get('value')

    @cache_on_tmp()
    def person_raw(self, person_id, person_fields=None):
        if person_fields is None:
            person_fields = 'names,emailAddresses'
        elif person_fields == 'all':
            fields_list = [
                'addresses', 'ageRanges', 'biographies', 'birthdays', 'calendarUrls', 'clientData', 'coverPhotos',
                'emailAddresses', 'events', 'externalIds', 'genders', 'imClients', 'interests', 'locales', 'locations',
                'memberships', 'metadata', 'miscKeywords', 'names', 'nicknames', 'occupations', 'organizations',
                'phoneNumbers', 'photos', 'relations', 'sipAddresses', 'skills', 'urls', 'userDefined'
            ]
            person_fields = ','.join(fields_list)

        resource_name = f'people/{person_id}'
        return self.people().get(resourceName=resource_name, personFields=person_fields).execute()