from random_service import RandomService


def main():
    rs = RandomService(seed=42)

    print("=== 随机整数 ===")
    for _ in range(5):
        print(f"  {rs.random_int(1, 100)}")

    print("\n=== 随机浮点数 ===")
    for _ in range(5):
        print(f"  {rs.random_float(0.0, 10.0):.4f}")

    print("\n=== 随机选择列表元素 ===")
    fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
    print(f"  随机选一个: {rs.random_choice(fruits)}")
    print(f"  随机选3个(可重复): {rs.random_choices(fruits, k=3)}")
    print(f"  随机抽3个(不重复): {rs.random_sample(fruits, k=3)}")

    print("\n=== 随机打乱列表 ===")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"  原列表: {numbers}")
    shuffled = rs.shuffle(numbers)
    print(f"  打乱后: {shuffled}")
    print(f"  原列表不变: {numbers}")

    print("\n=== 随机布尔值 ===")
    for _ in range(5):
        print(f"  {rs.random_bool()}")

    print("\n=== 随机字符串 ===")
    print(f"  8位字母数字: {rs.random_string(8)}")
    print(f"  6位数字: {rs.random_string(6, chars='0123456789')}")

    print("\n=== 随机范围(带步长) ===")
    for _ in range(5):
        print(f"  {rs.random_range(0, 100, 5)}")


if __name__ == "__main__":
    main()
