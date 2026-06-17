from random_service import RandomService


def demonstrate_basic():
    print("===== 基础随机数功能 =====\n")
    rs = RandomService()
    print(f"安全模式: {rs.is_secure}")
    print(f"随机整数 [1,100]: {rs.random_int(1, 100)}")
    print(f"随机浮点数 [0,10]: {rs.random_float(0, 10):.4f}")
    fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
    print(f"随机选择: {rs.random_choice(fruits)}")
    print(f"随机打乱 [1..5]: {rs.shuffle([1,2,3,4,5])}")


def demonstrate_distributions():
    print("\n\n===== 概率分布随机数 =====\n")
    rs = RandomService()

    print("1. 均匀分布 Uniform(low=0, high=10):")
    samples = rs.sample_distribution("uniform", 5, low=0, high=10)
    print(f"   样本: {[f'{x:.3f}' for x in samples]}")
    mean = sum(samples) / len(samples)
    print(f"   均值 ≈ 5 (理论值): {mean:.3f}")

    print("\n2. 正态分布 Normal(mu=100, sigma=15) - IQ 分布:")
    samples = rs.sample_distribution("normal", 1000, mu=100, sigma=15)
    print(f"   前5个样本: {[f'{x:.1f}' for x in samples[:5]]}")
    mean = sum(samples) / len(samples)
    variance = sum((x - mean) ** 2 for x in samples) / len(samples)
    std = variance ** 0.5
    print(f"   样本均值 ≈ 100: {mean:.2f}")
    print(f"   样本标准差 ≈ 15: {std:.2f}")
    below_85 = sum(1 for x in samples if x < 85)
    above_130 = sum(1 for x in samples if x > 130)
    print(f"   <85(智障) 比例 ≈ 15.87%: {below_85 / 10:.2f}%")
    print(f"   >130(天才) 比例 ≈ 2.28%: {above_130 / 10:.2f}%")

    print("\n3. 指数分布 Exponential(lambd=0.5) - 等待时间:")
    samples = rs.sample_distribution("exponential", 5, lambd=0.5)
    print(f"   样本: {[f'{x:.3f}' for x in samples]}")
    print(f"   理论均值 = 1/lambd = 2.0: {sum(samples)/len(samples):.3f}")

    print("\n4. 三角分布 Triangular(low=0, high=10, mode=3) - 项目估算:")
    samples = rs.sample_distribution("triangular", 5, low=0, high=10, mode=3)
    print(f"   样本: {[f'{x:.3f}' for x in samples]}")
    mean = sum(samples) / len(samples)
    print(f"   理论均值 = (0+3+10)/3 ≈ 4.33: {mean:.3f}")

    print("\n5. 对数正态分布 LogNormal(mu=0, sigma=1) - 收入分布:")
    samples = rs.sample_distribution("lognormal", 5, mu=0, sigma=1)
    print(f"   样本: {[f'{x:.3f}' for x in samples]}")

    print("\n6. Beta 分布 Beta(alpha=2, beta=5) - 概率建模:")
    samples = rs.sample_distribution("beta", 5, alpha=2, beta=5)
    print(f"   样本(均在[0,1]): {[f'{x:.3f}' for x in samples]}")

    print("\n7. Gamma 分布 Gamma(alpha=2, beta=2) - 排队模型:")
    samples = rs.sample_distribution("gamma", 5, alpha=2, beta=2)
    print(f"   样本: {[f'{x:.3f}' for x in samples]}")

    print("\n8. Pareto 分布 Pareto(alpha=2.0) - 80/20 法则:")
    samples = rs.sample_distribution("pareto", 5, alpha=2.0)
    print(f"   样本(长尾): {[f'{x:.3f}' for x in samples]}")

    print("\n9. Weibull 分布 Weibull(alpha=1.5, beta=1.0) - 寿命分析:")
    samples = rs.sample_distribution("weibull", 5, alpha=1.5, beta=1.0)
    print(f"   样本: {[f'{x:.3f}' for x in samples]}")

    print("\n10. Von Mises 分布 VonMises(mu=0, kappa=4) - 角度数据:")
    import math
    samples = rs.sample_distribution("vonmises", 5, mu=0, kappa=4)
    print(f"   样本(弧度, 集中在0附近): {[f'{x:.3f}' for x in samples]}")
    print(f"   样本(角度): {[f'{math.degrees(x):.1f}°' for x in samples]}")


def demonstrate_individual_calls():
    print("\n\n===== 单个分布方法调用 =====\n")
    rs = RandomService()

    print(f"uniform(0, 100):        {rs.uniform(0, 100):.4f}")
    print(f"normal(mu=50, sigma=10): {rs.normal(50, 10):.4f}")
    print(f"exponential(lambd=0.1):  {rs.exponential(0.1):.4f}")
    print(f"triangular(0, 100, 70):  {rs.triangular(0, 100, 70):.4f}")


def demonstrate_validation():
    print("\n\n===== 参数校验 =====\n")
    rs = RandomService()

    print("1. 正态分布 sigma <= 0 报错:")
    try:
        rs.normal(mu=0, sigma=0)
    except ValueError as e:
        print(f"   ✅ {e}")

    print("\n2. 指数分布 lambd <= 0 报错:")
    try:
        rs.exponential(lambd=0)
    except ValueError as e:
        print(f"   ✅ {e}")

    print("\n3. 三角分布 mode 超出范围报错:")
    try:
        rs.triangular(0, 10, mode=100)
    except ValueError as e:
        print(f"   ✅ {e}")

    print("\n4. 未知分布名称报错:")
    try:
        rs.sample_distribution("unknown", 5)
    except ValueError as e:
        print(f"   ✅ {e}")


def demonstrate_mode_comparison():
    print("\n\n===== 安全 vs 普通模式（分布同样适用）=====\n")

    secure_rs = RandomService(secure=True)
    normal_rs = RandomService(secure=False, seed=42)

    print("安全模式（不可预测）:")
    print(f"  normal(0,1) 样本1: {secure_rs.normal(0, 1):.6f}")
    print(f"  normal(0,1) 样本2: {secure_rs.normal(0, 1):.6f}")

    print("\n普通模式 seed=42（可复现）:")
    print(f"  normal(0,1) 样本1: {normal_rs.normal(0, 1):.6f}")
    print(f"  normal(0,1) 样本2: {normal_rs.normal(0, 1):.6f}")

    print("\n重新创建 seed=42 的普通模式实例:")
    normal_rs2 = RandomService(secure=False, seed=42)
    print(f"  normal(0,1) 样本1: {normal_rs2.normal(0, 1):.6f}  (与上面相同)")
    print(f"  normal(0,1) 样本2: {normal_rs2.normal(0, 1):.6f}  (与上面相同)")


def main():
    demonstrate_basic()
    demonstrate_distributions()
    demonstrate_individual_calls()
    demonstrate_validation()
    demonstrate_mode_comparison()


if __name__ == "__main__":
    main()
