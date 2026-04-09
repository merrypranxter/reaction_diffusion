"""
Parameter definitions for Gray-Scott reaction-diffusion.
Dataclasses for type safety and IDE completion.
"""
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass(frozen=True)
class PearsonType:
    """
    One of the 17 classified Gray-Scott pattern types.
    
    Attributes:
        symbol: Greek letter or Roman (e.g., "α", "π", "R")
        name: Human-readable description
        F: Feed rate parameter
        k: Kill rate parameter
        wolfram_class: Complexity class (1, 2, "2-a", 3, 4)
        oscillation: Temporal behavior ("none", "chaotic", "periodic", etc.)
        soliton_shape: Spatial structure ("spots", "stripes", "worms", etc.)
        description: Detailed behavior description
        tags: Searchable keywords
        alt_presets: Alternative (F,k) pairs producing similar behavior
    """
    symbol: str
    name: str
    F: float
    k: float
    wolfram_class: Any  # int or str "2-a"
    oscillation: str
    soliton_shape: str
    description: str
    tags: List[str]
    alt_presets: Optional[List[Dict[str, float]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for kwargs unpacking."""
        return {
            'F': self.F,
            'k': self.k,
        }

    def with_diffusion(self, Du: float = 1.0, Dv: float = 0.5) -> Dict[str, float]:
        """Get full parameter dict including diffusion coefficients."""
        return {
            'Du': Du,
            'Dv': Dv,
            'F': self.F,
            'k': self.k,
        }


@dataclass(frozen=True)
class NamedBehavior:
    """
    Famous named parameter combinations (e.g., "Mitosis", "Coral Growth").
    """
    name: str
    F: float
    k: float
    source: str
    tags: List[str]
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, float]:
        return {'F': self.F, 'k': self.k}


# ============================================================================
# PEARSON TYPES — All 17 Classified Variants
# ============================================================================

R = PearsonType(
    symbol="R",
    name="Uniform Red",
    F=0.014,
    k=0.057,
    wolfram_class=1,
    oscillation="none",
    soliton_shape="none",
    description="Evolves to uniform red (low u) state",
    tags=["trivial", "stable"],
    alt_presets=[{"F": 0.074, "k": 0.069}]
)

B = PearsonType(
    symbol="B",
    name="Uniform Blue",
    F=0.050,
    k=0.059,
    wolfram_class=1,
    oscillation="none",
    soliton_shape="none",
    description="Evolves to uniform blue (high u) state",
    tags=["trivial", "stable"],
    alt_presets=[{"F": 0.078, "k": 0.059}]
)

ALPHA = PearsonType(
    symbol="α",
    name="Wavelet Chaos",
    F=0.010,
    k=0.047,
    wolfram_class=3,
    oscillation="chaotic",
    soliton_shape="wavelets",
    description="Spatiotemporal chaos of wavelets and fledgling spirals that repeatedly grow and annihilate",
    tags=["chaotic", "dynamic", "wavelets", "spirals"],
    alt_presets=[{"F": 0.014, "k": 0.053}]
)

BETA = PearsonType(
    symbol="β",
    name="Ocean Voids",
    F=0.014,
    k=0.039,
    wolfram_class=3,
    oscillation="chaotic",
    soliton_shape="waves",
    description="Waves on a blue ocean with periodic red voids that open suddenly and fill in",
    tags=["chaotic", "dynamic", "waves", "voids"],
    alt_presets=[{"F": 0.026, "k": 0.051}]
)

GAMMA = PearsonType(
    symbol="γ",
    name="Unstable Stripes",
    F=0.022,
    k=0.051,
    wolfram_class=3,
    oscillation="periodic_dU",
    soliton_shape="stripes",
    description="Wormlike or branching stripes with endless instability from overcrowding and grain boundary events",
    tags=["chaotic", "stripes", "branching", "worms"],
    alt_presets=[{"F": 0.026, "k": 0.055}]
)

DELTA = PearsonType(
    symbol="δ",
    name="Turing Spots",
    F=0.030,
    k=0.055,
    wolfram_class="2-a",
    oscillation="none",
    soliton_shape="negative_spots_hexagonal",
    description="True Turing patterns: hexagonal array of negative spots with stable grain boundaries",
    tags=["stable", "turing", "hexagonal", "spots", "negative", "classic"],
    alt_presets=[{"F": 0.042, "k": 0.059}]
)

EPSILON = PearsonType(
    symbol="ε",
    name="Chaotic Mitosis",
    F=0.018,
    k=0.055,
    wolfram_class=3,
    oscillation="chaotic",
    soliton_shape="spots",
    description="Spots resembling unstable solitons: rings grow until contact, spots split via mitosis, overcrowding causes die-outs",
    tags=["chaotic", "spots", "mitosis", "rings", "dynamic"],
    alt_presets=[{"F": 0.022, "k": 0.059}]
)

ZETA = PearsonType(
    symbol="ζ",
    name="Stable Chaotic Spots",
    F=0.022,
    k=0.061,
    wolfram_class=3,
    oscillation="subtle",
    soliton_shape="spots",
    description="Like epsilon but spots are more symmetrical and stable; disturbances affect smaller percentage of domain",
    tags=["chaotic", "spots", "semi-stable"],
    alt_presets=[{"F": 0.026, "k": 0.059}]
)

ETA = PearsonType(
    symbol="η",
    name="Spots and Worms",
    F=0.034,
    k=0.063,
    wolfram_class=3,
    oscillation="periodic_dU_then_stops",
    soliton_shape="mixed_spots_worms",
    description="Mix of spots and short worms; longer stripes break up; reaches steady state after extended run",
    tags=["mixed", "spots", "worms", "transient_chaos"],
    alt_presets=[]
)

THETA = PearsonType(
    symbol="θ",
    name="Ring Growth Stripes",
    F=0.030,
    k=0.057,
    wolfram_class="2-a",
    oscillation="transient",
    soliton_shape="negative_stripes_network",
    description="Blue spots grow into concentric rings; stripes grow widthwise into parallel/cross stripes; final state mostly connected network",
    tags=["stable", "stripes", "rings", "negative", "network"],
    alt_presets=[{"F": 0.038, "k": 0.061}]
)

IOTA = PearsonType(
    symbol="ι",
    name="Molecular Negatons",
    F=0.046,
    k=0.0594,
    wolfram_class=2,
    oscillation="none",
    soliton_shape="negatons",
    description="Negative spots (negatons) with molecule-like interaction; solitary negatons are not viable",
    tags=["stable", "negatons", "molecular", "negative"],
    alt_presets=[]
)

KAPPA = PearsonType(
    symbol="κ",
    name="Hedgerow Mazes",
    F=0.050,
    k=0.063,
    wolfram_class="2-a",
    oscillation="none",
    soliton_shape="stripes_branching",
    description="Stripes grow by developing meanders; form disconnected hedgerow-maze patterns with branching",
    tags=["stable", "stripes", "branching", "mazes"],
    alt_presets=[{"F": 0.058, "k": 0.063}]
)

LAMBDA = PearsonType(
    symbol="λ",
    name="Mitotic Hexagons",
    F=0.026,
    k=0.061,
    wolfram_class="2-a",
    oscillation="none",
    soliton_shape="spots_hexagonal",
    description="Solitons grow by mitosis (cell-division); arrange into hexagonal grids; eventually reach steady state",
    tags=["stable", "spots", "mitosis", "hexagonal"],
    alt_presets=[{"F": 0.034, "k": 0.065}]
)

MU = PearsonType(
    symbol="μ",
    name="Growing Worms",
    F=0.046,
    k=0.065,
    wolfram_class="2-a",
    oscillation="none",
    soliton_shape="worms",
    description="Stripes grow from each end (worms); co-exist with inert solitons; reorganize toward parallel stripes",
    tags=["stable", "worms", "stripes", "parallel"],
    alt_presets=[{"F": 0.058, "k": 0.065}]
)

NU = PearsonType(
    symbol="ν",
    name="Inert Solitons",
    F=0.054,
    k=0.067,
    wolfram_class=2,
    oscillation="none",
    soliton_shape="solitons_static",
    description="Non-mitotic solitons that drift apart exponentially slowly; steady state requires astronomical time",
    tags=["stable", "solitons", "static", "slow"],
    alt_presets=[{"F": 0.082, "k": 0.063}]
)

XI = PearsonType(
    symbol="ξ",
    name="Spirals",
    F=0.010,
    k=0.041,
    wolfram_class=3,
    oscillation="sustained_spiral",
    soliton_shape="spirals",
    description="Large sustained spirals similar to Belousov-Zhabotinsky reaction; spiral seeds are rare and essential",
    tags=["chaotic", "spirals", "BZ-like", "dynamic"],
    alt_presets=[{"F": 0.014, "k": 0.047}]
)

PI = PearsonType(
    symbol="π",
    name="U-Skate World",
    F=0.062,
    k=0.061,
    wolfram_class=4,
    oscillation="complex",
    soliton_shape="mixed_negative",
    description="THE richest type: negative stripes, loops, and spots forming stable localized structures, both moving and stationary, with oscillating force-like interactions",
    tags=["complex", "class4", "moving", "localized", "u-skate", "computational"],
    alt_presets=[{"F": 0.060, "k": 0.0609}]
)

RHO = PearsonType(
    symbol="ρ",
    name="Red Soap Bubbles",
    F=0.090,
    k=0.059,
    wolfram_class="2-a",
    oscillation="none",
    soliton_shape="bubbles_red",
    description="Closed red soap bubbles bordered by stripes with surface tension; smaller bubbles shrink, larger grow",
    tags=["stable", "bubbles", "surface_tension", "stripes"],
    alt_presets=[{"F": 0.102, "k": 0.055}]
)

SIGMA = PearsonType(
    symbol="σ",
    name="Blue Soap Bubbles",
    F=0.090,
    k=0.057,
    wolfram_class="2-a",
    oscillation="none",
    soliton_shape="bubbles_blue",
    description="Closed blue soap bubbles bordered by negative stripes; like rho with colors reversed; worm tips always shrink",
    tags=["stable", "bubbles", "surface_tension", "negative_stripes"],
    alt_presets=[{"F": 0.110, "k": 0.0523}]
)

# List of all types for iteration
ALL_PEARSON_TYPES = [
    R, B, ALPHA, BETA, GAMMA, DELTA, EPSILON, ZETA, ETA,
    THETA, IOTA, KAPPA, LAMBDA, MU, NU, XI, PI, RHO, SIGMA
]

# ============================================================================
# NAMED BEHAVIORS — Famous Parameter Combinations
# ============================================================================

MITOSIS = NamedBehavior(
    name="Mitosis",
    F=0.0367,
    k=0.0649,
    source="Karl Sims",
    tags=["classic", "biological"],
    description="Spots grow and divide like biological cells"
)

CORAL_GROWTH = NamedBehavior(
    name="Coral Growth",
    F=0.0545,
    k=0.062,
    source="Karl Sims",
    tags=["classic", "biological", "branching"],
    description="Branching coral-like structures"
)

U_SKATE_WORLD = NamedBehavior(
    name="U-Skate World",
    F=0.060,
    k=0.0609,
    source="Munafo 2009",
    tags=["complex", "moving", "class4"],
    description="Stable localized moving patterns (Munafo discovery)"
)

SOAP_BUBBLES = NamedBehavior(
    name="Soap Bubbles",
    F=0.090,
    k=0.059,
    source="Munafo",
    tags=["surface_tension"],
    description="Closed regions with surface-tension stripe borders"
)

WORMS = NamedBehavior(
    name="Worms",
    F=0.046,
    k=0.065,
    source="Pearson",
    tags=["growing", "parallel"],
    description="Stripes growing from their endpoints"
)

CLASSIC_TURING = NamedBehavior(
    name="Classic Turing",
    F=0.030,
    k=0.055,
    source="Pearson/Turing",
    tags=["hexagonal", "classic"],
    description="Hexagonal Turing pattern with grain boundaries"
)

BZ_SPIRALS = NamedBehavior(
    name="BZ Spirals",
    F=0.010,
    k=0.041,
    source="Munafo",
    tags=["spirals", "dynamic"],
    description="Spiral waves reminiscent of BZ chemical reaction"
)

HEDGEROW_MAZES = NamedBehavior(
    name="Hedgerow Mazes",
    F=0.050,
    k=0.063,
    source="Pearson",
    tags=["mazes", "branching"],
    description="Disconnected branching stripe networks"
)

CHAOTIC_SPOTS = NamedBehavior(
    name="Chaotic Spots",
    F=0.018,
    k=0.055,
    source="Pearson",
    tags=["chaotic", "mitosis"],
    description="Spots with endless mitosis and die-off cycles"
)

MOVING_SPOTS = NamedBehavior(
    name="Moving Spots (Gliders)",
    F=0.014,
    k=0.054,
    source="VisualPDE",
    tags=["moving", "dynamic"],
    description="Spots that bob around; increase k slowly to ~0.056"
)

LIMBNET_STRIPES = NamedBehavior(
    name="LimbNET Stripes",
    F=0.032,
    k=0.059,
    source="LimbNET/EMBL",
    tags=["stripes", "clean"],
    description="Clean parallel/branching stripes"
)

LIMBNET_DOTS = NamedBehavior(
    name="LimbNET Dots",
    F=0.028,
    k=0.062,
    source="LimbNET/EMBL",
    tags=["dots", "regular"],
    description="Regular spotted pattern"
)

ALL_NAMED_BEHAVIORS = [
    MITOSIS, CORAL_GROWTH, U_SKATE_WORLD, SOAP_BUBBLES, WORMS,
    CLASSIC_TURING, BZ_SPIRALS, HEDGEROW_MAZES, CHAOTIC_SPOTS,
    MOVING_SPOTS, LIMBNET_STRIPES, LIMBNET_DOTS
]
