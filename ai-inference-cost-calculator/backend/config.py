"""GPU specs, cloud pricing, and presets."""

GPUS = {
    "RTX 4090": {"cost": 1600, "watts": 350, "vram": 24},
    "RTX 3090": {"cost": 900, "watts": 350, "vram": 24},
    "A6000": {"cost": 4500, "watts": 300, "vram": 48},
    "A100 40GB": {"cost": 10000, "watts": 400, "vram": 40},
    "A100 80GB": {"cost": 15000, "watts": 400, "vram": 80},
    "H100": {"cost": 30000, "watts": 700, "vram": 80},
}

CLOUD_PROVIDERS = {
    "RunPod": {"rtx4090": 0.39, "rtx3090": 0.31, "a6000": 0.79, "a100_40gb": 1.64, "a100_80gb": 1.94, "h100": 2.49},
    "Lambda Labs": {"rtx4090": 0.50, "rtx3090": 0.40, "a6000": 0.80, "a100_40gb": 1.29, "a100_80gb": 1.79, "h100": 2.49},
    "AWS": {"rtx4090": 0.80, "rtx3090": 0.65, "a6000": 1.10, "a100_40gb": 2.06, "a100_80gb": 2.48, "h100": 3.99},
    "GCP": {"rtx4090": 0.75, "rtx3090": 0.60, "a6000": 1.05, "a100_40gb": 1.94, "a100_80gb": 2.35, "h100": 3.74},
}

GPU_KEY_MAP = {
    "RTX 4090": "rtx4090",
    "RTX 3090": "rtx3090",
    "A6000": "a6000",
    "A100 40GB": "a100_40gb",
    "A100 80GB": "a100_80gb",
    "H100": "h100",
}

PRESETS = {
    "Custom": None,
    "Hobbyist (100/day)": 100,
    "Startup (10k/day)": 10_000,
    "Enterprise (1M/day)": 1_000_000,
}
