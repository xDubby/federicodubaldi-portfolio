from dataclasses import dataclass

@dataclass(frozen=True)
class NoiseProfile:
    name: str

    # % righe duplicate
    dup_rate: float

    # % righe con valori mancanti (random columns)
    missing_rate: float

    # % righe con valori “sporchi” (prezzi / date / numeri come stringhe ecc.)
    dirty_rate: float

    # % righe con outlier su price
    outlier_rate: float

    # probabilità di rinominare alcune colonne (schema drift)
    rename_schema: bool

PROFILES = {
    "light": NoiseProfile(
        name="light",
        dup_rate=0.01,
        missing_rate=0.01,
        dirty_rate=0.02,
        outlier_rate=0.005,
        rename_schema=True,
    ),
    "medium": NoiseProfile(
        name="medium",
        dup_rate=0.03,
        missing_rate=0.03,
        dirty_rate=0.06,
        outlier_rate=0.01,
        rename_schema=True,
    ),
    "hard": NoiseProfile(
        name="hard",
        dup_rate=0.06,
        missing_rate=0.06,
        dirty_rate=0.12,
        outlier_rate=0.03,
        rename_schema=True,
    ),
}
