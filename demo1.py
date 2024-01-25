from api_demo_origin_1 import MockService

# S1
s1 = MockService('user1', 'secret1')
s1_res1 = s1.add_item({
    "item_id": 1,
    "item_name": "item name"
})
assert s1_res1.status_code == 201

s1_res2 = s1.get_item("1")
assert s1_res2.status_code == 200