import random
from typing import Any, List, Optional, Sequence, Tuple


class RandomService:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def random_int(self, low: int, high: int) -> int:
        if low > high:
            low, high = high, low
        return random.randint(low, high)

    def random_float(self, low: float = 0.0, high: float = 1.0) -> float:
        if low > high:
            low, high = high, low
        return random.uniform(low, high)

    def random_choice(self, seq: Sequence[Any]) -> Any:
        if not seq:
            raise ValueError("序列不能为空")
        return random.choice(seq)

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
        return random.choices(seq, weights=weights, k=k)

    def random_sample(self, seq: Sequence[Any], k: int) -> List[Any]:
        if not seq:
            raise ValueError("序列不能为空")
        if k <= 0 or k > len(seq):
            raise ValueError("k 必须在 1 到序列长度之间")
        return random.sample(seq, k)

    def shuffle(self, lst: List[Any]) -> List[Any]:
        if not isinstance(lst, list):
            raise TypeError("参数必须是列表类型")
        shuffled = lst.copy()
        random.shuffle(shuffled)
        return shuffled

    def shuffle_inplace(self, lst: List[Any]) -> None:
        if not isinstance(lst, list):
            raise TypeError("参数必须是列表类型")
        random.shuffle(lst)

    def random_bool(self, probability: float = 0.5) -> bool:
        if not 0 <= probability <= 1:
            raise ValueError("概率必须在 0 到 1 之间")
        return random.random() < probability

    def random_string(
        self,
        length: int,
        chars: Optional[str] = None,
    ) -> str:
        if length <= 0:
            raise ValueError("长度必须大于 0")
        if chars is None:
            import string
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def random_range(self, start: int, stop: int, step: int = 1) -> int:
        if step == 0:
            raise ValueError("步长不能为 0")
        return random.randrange(start, stop, step)
