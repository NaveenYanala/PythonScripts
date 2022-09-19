import json
import re


class AmbariPrimaryView:
    def __init__(self, user, query, status, hive_query_id, tables_read, max_scan_date, query_start_time,
                 query_end_time):
        self.user = user
        self.query = query
        self.status = status
        self.hive_query_id = hive_query_id
        self.tables_read = ",".join(tables_read)
        self.max_scan_date = max_scan_date
        self.rundate = self.parse_key(self.hive_query_id)
        self.query_end_time = query_end_time
        self.query_start_time = query_start_time
        self.query_run_time = self.query_end_time -self.query_start_time if self.query_end_time !=0 else 0
    def __str__(self):
        return f'{self.user},{self.status},{self.hive_query_id},"{self.tables_read}",{self.max_scan_date},{self.rundate},' \
               f'{self.query_start_time},{self.query_end_time},{self.query_run_time}\n'

    def __repr__(self):
        return f'{self.user},{self.status},{self.hive_query_id},"{self.tables_read}",{self.max_scan_date},{self.rundate},{self.query_start_time},' \
               f'{self.query_end_time},{self.query_run_time}\n'

    @staticmethod
    def parse_key(key):
        p = key[5:13]
        if key == 't-prod_2':
            pass
        return p


class AmbariView:

    def __init__(self, list_data):
        self.list_data = list_data
        self.ambari_primary_view_queries = dict()

    def parse(self):
        # print("hi at 41")

        for data in self.list_data:
            self.data = data
            # print(data)
            # exit()
            self.entities = self.data['entities']
            for entity in self.entities:
                self.primary_filter = entity['primaryfilters']
                self.user = self.primary_filter['requestuser'][0]
                self.tablesread = self.primary_filter['tablesread'] if 'tablesread' in self.primary_filter else ""
                self.query = json.loads(entity['otherinfo']['QUERY'])['queryText'] if 'QUERY' in entity[
                    'otherinfo'] else ""
                self.get_max_date_filters()
                self.hive_query_id = entity['entity']
                self.max_scan_date = self.get_max_date_filters()
                if len(entity['events']) == 2:
                    self.latest_event = entity['events'][0]
                    self.query_status = self.latest_event['eventtype']
                    self.query_end_time = self.latest_event['timestamp']
                    self.query_start_time = entity['events'][1]['timestamp']
                else:
                    self.latest_event = entity['events'][0]
                    self.query_status = self.latest_event['eventtype']
                    self.query_start_time = self.latest_event['timestamp']
                    self.query_end_time = 0
                a = AmbariPrimaryView(self.user, self.query, self.query_status, self.hive_query_id, self.tablesread,
                                      self.max_scan_date, self.query_start_time, self.query_end_time)

                if self.hive_query_id in self.ambari_primary_view_queries :
                    a.query = self.ambari_primary_view_queries[self.hive_query_id].query
                self.ambari_primary_view_queries[self.hive_query_id] = a
        # print(entity('primaryfilters'))
        return self.ambari_primary_view_queries

    def get_max_date_filters(self):

        last_part = "NA"
        if 'where' in self.query:
            last_part = self.query.split("where")[1]
        elif 'WHERE' in self.query:
            last_part = self.query.split("WHERE")[1]
        if "NA" != last_part:
            match = re.findall(r'\d{4}-\d{2}-\d{2}', last_part)

            # print(f"last macth {last_part}")

            if len(match) != 0:
                match.sort()
                # print(f"date {match}")
                return match[0]

        return "1900-01-01"
