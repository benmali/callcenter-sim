from collections import OrderedDict
calls = OrderedDict({'0.0': 225, '0.5': 85, '1.0': 70, '1.5': 80, '2.0': 40,
                                '2.5': 29, '3.0': 40, '3.5': 35, '4.0': 37, '4.5': 36, '5.0': 11,
                                '5.5': 21, '6.0': 14, '6.5': 7, '7.0': 7, '7.5': 8, '8.0': 7, '8.5': 7, '9.0': 5,
                                '9.5': 8, '10.0': 3, '10.5': 1, '12.0': 1})

chats = OrderedDict({'0.0': 225, '0.5': 90, '1.0': 80, '1.5': 70, '2.0': 50,
                                '2.5': 40, '3.0': 30, '3.5': 25, '4.0': 20, '4.5': 17, '5.0': 11,
                                '5.5': 21, '6.0': 14, '6.5': 7, '7.0': 7, '7.5': 8, '8.0': 7, '8.5': 7, '9.0': 5,
                                '9.5': 8, '10.0': 3, '10.5': 1, '12.0': 1})
print(sum(chats.values()))
c = 0
avg = 0
base_calls = 1055
base_chats = 1168
n_call_agent = 15
n_chat_agent = 15
base_call_ratio = base_calls / n_call_agent
base_chat_ratio = base_chats / n_chat_agent
n_actual_calls = 1067
n_actual_call_agents = 14
n_actual_chats = 1200
n_actual_chat_agents = 14
actual_call_ratio = n_actual_calls / n_actual_call_agents
actual_chat_ratio = n_actual_chats / n_actual_chat_agents

z = [0.1, -0.05, 0.1, 0.05]
multi_call_weights = [x * (actual_call_ratio / base_call_ratio) for x in z]
multi_chat_weights = [x * (actual_chat_ratio / base_call_ratio) for x in z]
call_weights = [float(n_ppl) / sum(calls.values()) for n_ppl in calls.values() ]
chat_weights = [float(n_ppl) / sum(chats.values()) for n_ppl in chats.values() ]

drop_from_first = 0.2  # mulitpy 0.2 * weight of first
base_rest = base_calls * 0.03


weights = []
for key, value in calls.items():
    c += value
    avg += float(key) * value
print(c)
print(avg / sum(calls.values()))
base_weights = []