import random
import secrets
import string
from typing import Any, List, Optional, Sequence


class RandomService:
    def __init__(
        self,
        secure: bool = True,
        seed: Optional[int] = None,
    ):
        self._secure = secure
        if secure:
            if seed is not None:
                raise ValueError(
                    "安全模式下不支持设置 seed，否则随机数将可预测"
                )
            self._rng: random.Random = secrets.SystemRandom()
        else:
            self._rng = random.Random(seed)

    @property
    def is_secure(self) -> bool:
        return self._secure

    def random_int(self, low: int, high: int) -> int:
        if low > high:
            low, high = high, low
        return self._rng.randint(low, high)

    def random_float(self, low: float = 0.0, high: float = 1.0) -> float:
        if low > high:
            low, high = high, low
        return self._rng.uniform(low, high)

    def random_choice(self, seq: Sequence[Any]) -> Any:
        if not seq:
            raise ValueError("序列不能为空")
        return self._rng.choice(seq)

    def random_choices(
        self,
        seq: Sequence[Any],
        k: int = 1,
        weights: Optional[List[float]] = None,
    ) -> List[Any]:
        if not seq:
            raise ValueError("序列不能为空")
        if k <= 0:
            return []
        if weights is not None and len(weights) != len(seq):
            raise ValueError("权重列表长度必须与序列长度一致")
        return self._rng.choices(seq, weights=weights, k=k)

    def random_sample(self, seq: Sequence[Any], k: int) -> List[Any]:
        if not seq:
            raise ValueError("序列不能为空")
        if k <= 0 or k > len(seq):
            raise ValueError("k 必须在 1 到序列长度之间")
        return self._rng.sample(seq, k)

    def shuffle(self, lst: List[Any]) -> List[Any]:
        if not isinstance(lst, list):
            raise TypeError("参数必须是列表类型")
        shuffled = lst.copy()
        self._rng.shuffle(shuffled)
        return shuffled

    def shuffle_inplace(self, lst: List[Any]) -> None:
        if not isinstance(lst, list):
            raise TypeError("参数必须是列表类型")
        self._rng.shuffle(lst)

    def random_bool(self, probability: float = 0.5) -> bool:
        if not 0 <= probability <= 1:
            raise ValueError("概率必须在 0 到 1 之间")
        return self._rng.random() < probability

    def random_string(
        self,
        length: int,
        chars: Optional[str] = None,
    ) -> str:
        if length <= 0:
            raise ValueError("长度必须大于 0")
        if chars is None:
            chars = string.ascii_letters + string.digits
        return ''.join(self._rng.choice(chars) for _ in range(length))

    def random_range(self, start: int, stop: int, step: int = 1) -> int:
        if step == 0:
            raise ValueError("步长不能为 0")
        return self._rng.randrange(start, stop, step)

    def random_below(self, n: int) -> int:
        if n <= 0:
            raise ValueError("n 必须大于 0")
        if self._secure:
            return secrets.randbelow(n)
        return self._rng.randrange(n)

    def random_token_hex(self, nbytes: int = 16) -> str:
        if not self._secure:
            raise RuntimeError(
                "random_token_hex 仅在安全模式下可用"
            )
        return secrets.token_hex(nbytes)

    def random_token_urlsafe(self, nbytes: int = 16) -> str:
        if not self._secure:
            raise RuntimeError(
                "random_token_urlsafe 仅在安全模式下可用"
            )
        return secrets.token_urlsafe(nbytes)

    def compare_digest(self, a: str, b: str) -> bool:
        return secrets.compare_digest(a, b)

    def uniform(self, low: float = 0.0, high: float = 1.0) -> float:
        if low > high:
            low, high = high, low
        return self._rng.uniform(low, high)

    def normal(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        if sigma <= 0:
            raise ValueError("标准差 sigma 必须大于 0")
        return self._rng.gauss(mu, sigma)

    def gauss(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        return self.normal(mu, sigma)

    def exponential(self, lambd: float = 1.0) -> float:
        if lambd <= 0:
            raise ValueError("参数 lambd 必须大于 0")
        return self._rng.expovariate(lambd)

    def triangular(
        self,
        low: float = 0.0,
        high: float = 1.0,
        mode: Optional[float] = None,
    ) -> float:
        if low > high:
            low, high = high, low
        if mode is not None and not (low <= mode <= high):
            raise ValueError("mode 必须在 [low, high] 范围内")
        return self._rng.triangular(low, high, mode)

    def beta(self, alpha: float, beta: float) -> float:
        if alpha <= 0 or beta <= 0:
            raise ValueError("alpha 和 beta 必须大于 0")
        return self._rng.betavariate(alpha, beta)

    def gamma(self, alpha: float, beta: float) -> float:
        if alpha <= 0 or beta <= 0:
            raise ValueError("alpha 和 beta 必须大于 0")
        return self._rng.gammavariate(alpha, beta)

    def lognormal(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        if sigma <= 0:
            raise ValueError("标准差 sigma 必须大于 0")
        return self._rng.lognormvariate(mu, sigma)

    def pareto(self, alpha: float) -> float:
        if alpha <= 0:
            raise ValueError("alpha 必须大于 0")
        return self._rng.paretovariate(alpha)

    def weibull(self, alpha: float, beta: float) -> float:
        if alpha <= 0 or beta <= 0:
            raise ValueError("alpha 和 beta 必须大于 0")
        return self._rng.weibullvariate(alpha, beta)

    def vonmises(self, mu: float, kappa: float) -> float:
        if kappa <= 0:
            raise ValueError("kappa 必须大于 0")
        return self._rng.vonmisesvariate(mu, kappa)

    def sample_distribution(
        self,
        name: str,
        count: int,
        **params,
    ) -> List[float]:
        if count <= 0:
            raise ValueError("count 必须大于 0")
        dist_map = {
            "uniform": self.uniform,
            "normal": self.normal,
            "gauss": self.normal,
            "exponential": self.exponential,
            "triangular": self.triangular,
            "beta": self.beta,
            "gamma": self.gamma,
            "lognormal": self.lognormal,
            "pareto": self.pareto,
            "weibull": self.weibull,
            "vonmises": self.vonmises,
        }
        if name not in dist_map:
            raise ValueError(
                f"不支持的分布 '{name}'，支持: {', '.join(dist_map.keys())}"
            )
        func = dist_map[name]
        return [func(**params) for _ in range(count)]
