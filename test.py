# dict1 = {1: {"asd": 3}, 2: {}}
# dict2 = {1: {"asda": 2}, 2: {}}

# # for key in set(dict1) & set(dict2):
# #     if dict1[key].keys() & dict2[key].keys():
# #         ut.RAISE(f"Duplicate keys found within subdictionaries for key {key}")
    
# if any(dict1[key].keys() & dict2[key].keys() for key in set(dict1) & set(dict2)):
#     ut.RAISE("Duplicate keys found within subdictionaries")


# merged_dict = {k: {**dict1.get(k, {}), **dict2.get(k, {})} for k in set(dict1) | set(dict2)}

# print(merged_dict)



# original_dict = {"a": [1, 2, 3], "b": [4, 5], "c": 6}

# # flipped_dict = {}
# # for key, value in original_dict.items():
# #     for item in value:
# #         flipped_dict[item] = key

# flipped_dict = {item: key for key, value in original_dict.items() for item in value}


# original_dict = {"a": [1, 2, 3], "b": [4, 5], "c": 6}

# flipped_dict = {item: key for key, value in original_dict.items() for item in ([value] if isinstance(value, int) else value)}


# print(flipped_dict)



# from MarketHelper import MarketHelper
# from RefHelper import RefereesHelper

# referees_helper_instance1 = RefereesHelper()
# referees_helper_instance2 = RefereesHelper()
# print(referees_helper_instance1 is referees_helper_instance2)  # This should print True



# market_helper_instance1 = MarketHelper()
# market_helper_instance2 = MarketHelper()
# print(market_helper_instance1 is market_helper_instance2)  # This should print True



# print(referees_helper_instance1.CURRENT_REFEREE_ID)
# print(referees_helper_instance2.CURRENT_REFEREE_ID)
# referees_helper_instance2.CURRENT_REFEREE_ID+=1
# print(referees_helper_instance1.CURRENT_REFEREE_ID)
# print(referees_helper_instance2.CURRENT_REFEREE_ID)