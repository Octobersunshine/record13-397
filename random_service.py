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
