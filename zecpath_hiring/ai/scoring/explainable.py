def weighted_score(components: dict[str, float], weights: dict[str, float]) -> dict:
    total_weight = sum(weights.values()) or 1.0
    weighted_total = sum(components[name] * weights.get(name, 0.0) for name in components)
    final_score = round(weighted_total / total_weight, 2)
    return {
        "components": components,
        "weights": weights,
        "final_score": final_score,
        "explanation": [
            f"{name} contributed {round(components[name] * weights.get(name, 0.0), 2)}"
            for name in components
        ],
    }

