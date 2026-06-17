from random_service import RandomService


def demonstrate_secure_mode():
    print("===== 安全模式 (默认，使用 secrets 模块) =====\n")
    rs = RandomService(secure=True)
    print(f"是否安全模式: {rs.is_secure}")

    print("\n1. 随机整数:")
    for _ in range(3):
        print(f"   {rs.random_int(1, 100)}")

    print("\n2. 随机浮点数:")
    for _ in range(3):
        print(f"   {rs.random_float(0.0, 10.0):.4f}")

    print("\n3. 随机选择列表元素:")
    fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
    print(f"   随机选一个: {rs.random_choice(fruits)}")
    print(f"   随机抽3个(不重复): {rs.random_sample(fruits, k=3)}")

    print("\n4. 随机打乱列表:")
    numbers = [1, 2, 3, 4, 5]
    print(f"   原列表: {numbers}")
    print(f"   打乱后: {rs.shuffle(numbers)}")

    print("\n5. 安全随机数 (secrets 特有):")
    print(f"   randbelow(100): {rs.random_below(100)}")
    print(f"   token_hex(16): {rs.random_token_hex(16)}")
    print(f"   token_urlsafe(16): {rs.random_token_urlsafe(16)}")

    print("\n6. 安全比较 (防时序攻击):")
    token1 = rs.random_token_hex(8)
    token2 = rs.random_token_hex(8)
    print(f"   compare_digest({token1[:8]}..., {token1[:8]}...): "
          f"{rs.compare_digest(token1, token1)}")
    print(f"   compare_digest({token1[:8]}..., {token2[:8]}...): "
          f"{rs.compare_digest(token1, token2)}")


def demonstrate_normal_mode():
    print("\n\n===== 普通模式 (使用 random 模块，可预测) =====\n")

    rs1 = RandomService(secure=False, seed=42)
    print(f"是否安全模式: {rs1.is_secure}")
    print(f"seed=42 的随机序列:")
    print(f"   int: {rs1.random_int(1, 100)}")
    print(f"   float: {rs1.random_float(0, 10):.4f}")
    print(f"   choice: {rs1.random_choice(['a', 'b', 'c'])}")

    print("\n使用相同 seed=42 再次创建实例:")
    rs2 = RandomService(secure=False, seed=42)
    print(f"   int: {rs2.random_int(1, 100)}  (与上面相同，可预测)")
    print(f"   float: {rs2.random_float(0, 10):.4f}  (与上面相同，可预测)")
    print(f"   choice: {rs2.random_choice(['a', 'b', 'c'])}  (与上面相同，可预测)")

    print("\n⚠️  普通模式用于测试、模拟等可复现场景")
    print("⚠️  绝不能用于密码、令牌、抽奖等安全敏感场景")


def demonstrate_security_checks():
    print("\n\n===== 安全防护验证 =====\n")

    print("1. 安全模式下设置 seed 会报错:")
    try:
        RandomService(secure=True, seed=42)
    except ValueError as e:
        print(f"   ✅ 错误: {e}")

    print("\n2. 普通模式下调用安全特有方法会报错:")
    rs = RandomService(secure=False)
    try:
        rs.random_token_hex()
    except RuntimeError as e:
        print(f"   ✅ 错误: {e}")


def main():
    demonstrate_secure_mode()
    demonstrate_normal_mode()
    demonstrate_security_checks()

    print("\n\n===== 最佳实践建议 =====\n")
    print("✅ 密码、验证码、Token、抽奖 → 使用 secure=True (默认)")
    print("✅ 单元测试、模拟数据 → 使用 secure=False + seed")
    print("❌ 永远不要在安全场景使用 random 模块或设置 seed")


if __name__ == "__main__":
    main()
