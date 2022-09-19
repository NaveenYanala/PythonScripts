# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# with io.open('hive.txt', 'a') as f:
#     for value in t.values():
#         f.write(str(value))
from AmbariViewDAO import AmbariView
from AmbariParser import AmbariParser

import io
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def total_number_of_query_per_day(daywise_total_query, t):
    all_keys = t.keys()
    for k in all_keys:
        parsed_date = parse_key(k)

        if parsed_date in daywise_total_query:
            daywise_total_query[parsed_date] = daywise_total_query[parsed_date] + 1
        else:
            daywise_total_query[parsed_date] = 1
    print(daywise_total_query)
    return daywise_total_query


def parse_key(key):
    p= key[5:13]
    if key=='t-prod_2':
        pass
    return p


def write(t):
    with io.open('hive.csv', 'w') as f:
        for value in t.values():
            # print(value)
            # print(str(value))
            f.write(str(value))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    daywise_total_query = dict()
    a = AmbariParser(1, 50)
    t = AmbariView(a.get_dag_summary()).parse()
    write(t)
  #  daywise_total_query = total_number_of_query_per_day(daywise_total_query, t)


    last_hive_query_id = list(t)[-1]

    while len(t) != 0:
        a = AmbariParser(1, 50, last_hive_query_id)
        t = AmbariView(a.get_dag_summary()).parse()
        # write(t)
      #  total_number_of_query_per_day(daywise_total_query, t)
      #   print(t)
        #print(last_hive_query_id)
        last_hive_query_id = list(t)[-1]

    print("done")





