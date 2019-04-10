from gsuite.GSuite import GSuite


class GSuite_Admin:

    def __init__(self):
        self.service = GSuite().admin_reports_v1()


    def get_api_data_raw(self, application, max_results=1000, page_token=None, start_time = None):
        return self.service.activities().list(userKey         = 'all'       ,
                                              applicationName = application ,
                                              maxResults      = max_results ,
                                              pageToken       = page_token  ,
                                              startTime       = start_time  ).execute()

    def get_api_data(self,  application, number_of_items_to_fetch = 100, max_results = 100):                # this doesn't scale for the calendar one since it has tons on entries
        all_items = []
        next_page_token = None
        if number_of_items_to_fetch > 1000:
            number_of_items_to_fetch = 1000         # this is limitation of gsuite logs

        def get_results(page_token):
            results = self.get_api_data_raw(application, number_of_items_to_fetch, page_token)
            all_items.extend(results['items'])
            return results.get('nextPageToken')

        next_page_token = get_results(next_page_token)

        while next_page_token is not None:
            if max_results is not None:
                if len (all_items) >= max_results:
                    break;
            next_page_token = get_results(next_page_token)

        return all_items