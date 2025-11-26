def knapsack_greedy():
    # 1. 定义物品列表 - 列表包含元组
    items = [
        ('r', 3, 25), ('p', 2, 15), ('a', 2, 15), ('m', 2, 20),
        ('i', 1, 5), ('k', 1, 15), ('x', 3, 20), ('t', 1, 25),
        ('f', 1, 15), ('d', 1, 10), ('s', 2, 20), ('c', 2, 20)
    ]

    # 2. 定义变量
    capacity = 8
    required_item = ('d', 1, 10)

    # 3. 初始化选择列表和计数器
    selected_items = []  # 存放选择的物品
    current_size = 0  # 当前已用容量
    total_value = 0  # 总价值

    # 4. 先加入必须包含的物品
    selected_items.append(required_item)
    current_size += required_item[1]  # required_item[1]是大小
    total_value +=  required_item[2]  #required_item[2]是价值

    # 5. 从原列表移除已选物品，避免重复选择
    remaining_items = [item for item in items if item != required_item]

    # 6. 按价值密度排序剩余物品
    sorted_items = sorted(remaining_items,
                          key=lambda x: x[2] / x[1],  # 按价值密度排序
                          reverse=True)  # 降序

    # 7. 贪心选择
    for item in sorted_items:
        name, size, value = item  # 解包元组

        # 检查容量
        if current_size + size <= capacity:
            selected_items.append(item)
            current_size += size
            total_value += value

            # 如果装满则提前结束
            if current_size == capacity:
                break

    # 8. 输出结果
    print("选择的物品:")
    for item in selected_items:
        print(f"  物品{item[0]}: 大小{item[1]}, 价值{item[2]}")

    print(f"总大小: {current_size}")
    print(f"总价值: {total_value}")

    return selected_items, total_value


# 调用函数
solution, value = knapsack_greedy()