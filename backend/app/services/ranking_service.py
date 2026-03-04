def calculate_rank_score(roi: float, sharpe_ratio: float, stake_amount: float) -> float:
    return (roi * 0.55) + (sharpe_ratio * 0.3) + (stake_amount * 0.15)
