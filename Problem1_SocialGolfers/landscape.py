
"""
Landscape analysis for Social Golfers Problem.

Ekzekutimi:
python Problem1_SocialGolfers/landscape.py

Perdor funksionet objective() dhe upper_bound()
nga social_golfers.py.
"""

import argparse
import math
import random
from collections import Counter

from social_golfers import objective, upper_bound


# 1. Madhesia e hapesires se kerkimit
def partitions_per_week(groups, size):
    """
    Numri i ndarjeve te ndryshme te lojtareve
    ne grupe brenda nje jave.
    """
    players = groups * size

    return math.factorial(players) // (
        math.factorial(size) ** groups
        * math.factorial(groups)
    )


# 2. Gjenerimi i orareve te rastësishme
def random_schedule(groups, size, weeks, rng):
    """
    Gjeneron nje orar ku secili lojtar paraqitet
    nje here per jave.

    Ciftet mund te perseriten ne jave te ndryshme.
    """
    players_count = groups * size
    schedule = []

    for _ in range(weeks):
        players = list(range(players_count))
        rng.shuffle(players)

        week = [
            players[i * size:(i + 1) * size]
            for i in range(groups)
        ]

        schedule.append(week)

    return schedule


# 3. Krijimi i nje zgjidhjeje fqinje
def random_neighbor(schedule, rng):
    """
    Nderron dy lojtare nga dy grupe te ndryshme
    brenda te njejtes jave.
    """
    neighbor = [
        [group[:] for group in week]
        for week in schedule
    ]

    week_index = rng.randrange(len(neighbor))

    group_a, group_b = rng.sample(
        range(len(neighbor[week_index])), 2
    )

    position_a = rng.randrange(
        len(neighbor[week_index][group_a])
    )

    position_b = rng.randrange(
        len(neighbor[week_index][group_b])
    )

    neighbor[week_index][group_a][position_a], \
    neighbor[week_index][group_b][position_b] = (
        neighbor[week_index][group_b][position_b],
        neighbor[week_index][group_a][position_a],
    )

    return neighbor


# 4. Histogrami i vlerave te Objective Function
def show_histogram(scores, max_bins=12):
    """
    Shfaq shperndarjen e vlerave f(S)
    ne forme histogrami tekstual.
    """
    minimum = min(scores)
    maximum = max(scores)

    bin_size = max(
        1,
        math.ceil(
            (maximum - minimum + 1) / max_bins
        )
    )

    frequency = Counter(
        (score - minimum) // bin_size
        for score in scores
    )

    highest = max(frequency.values())

    for bin_number in range(
        (maximum - minimum) // bin_size + 1
    ):
        start = minimum + bin_number * bin_size
        end = min(maximum, start + bin_size - 1)

        count = frequency[bin_number]

        bar = "#" * round(
            32 * count / highest
        )

        label = (
            str(start)
            if start == end
            else f"{start}-{end}"
        )

        print(
            f"  f(S)={label:>9}: "
            f"{count:>4}  {bar}"
        )


# 5. Analiza kryesore e Landscape
def analyze(
    groups,
    size,
    weeks,
    samples,
    neighbor_schedules,
    swaps_per_schedule,
    seed,
):

    rng = random.Random(seed)

    n = groups * size

    partitions = partitions_per_week(
        groups, size
    )

    bound = upper_bound(groups, size)

    total_pairs = math.comb(n, 2)

    pairs_per_week = (
        groups * math.comb(size, 2)
    )

    print(
        "=== SOCIAL GOLFERS: ANALIZA E LANDSCAPE ==="
    )

    print(
        f"Lojtare: {n} | "
        f"Grupe: {groups} | "
        f"Lojtare/grup: {size} | "
        f"Jave: {weeks}"
    )

    # Madhesia e hapesires se kerkimit
    print(
        "\n1. Madhesia e hapesires se kerkimit"
    )

    print(
        f"  Ndarje te ndryshme per nje jave, "
        f"P: {partitions:,}"
    )

    print(
        f"  Modeli naiv, n^(n*w): "
        f"~ 10^{n * weeks * math.log10(n):.2f}"
    )

    print(
        f"  Permutime, (n!)^w: "
        f"~ 10^{weeks * math.log10(math.factorial(n)):.2f}"
    )

    print(
        f"  Ndarje ne grupe, P^w: "
        f"~ 10^{weeks * math.log10(partitions):.2f}"
    )

    print(
        f"  Me javen e pare fikse: "
        f"~ 10^{(weeks - 1) * math.log10(partitions):.2f}"
    )

    print(
        "  SHENIM: Kjo eshte hapesira potenciale, "
        "jo numri i zgjidhjeve valide."
    )

    # Kufizimet nga ciftet
    print(
        "\n2. Kufizimi nga ciftet e lojtareve"
    )

    print(
        f"  Cifte te mundshme gjithsej: "
        f"{total_pairs}"
    )

    print(
        f"  Cifte te formuara per jave: "
        f"{pairs_per_week}"
    )

    print(
        f"  Kufiri teorik i javeve: {bound}"
    )

    print(
        f"  Cifte te nevojshme per {weeks} jave: "
        f"{weeks * pairs_per_week}"
    )

    print(
        f"  Perqindja e cifteve: "
        f"{100 * weeks * pairs_per_week / total_pairs:.1f}%"
    )

    if weeks > bound:
        print(
            "  KUJDES: Numri i javeve tejkalon "
            "kufirin teorik."
        )

    # Fitness Landscape
    print(
        f"\n3. Fitness landscape "
        f"({samples} orare te rastësishme)"
    )

    scores = [
        objective(
            random_schedule(
                groups, size, weeks, rng
            )
        )
        for _ in range(samples)
    ]

    print(
        f"  f(S) min: {min(scores)} | "
        f"max: {max(scores)}"
    )

    print(
        f"  f(S) mesatar: "
        f"{sum(scores) / len(scores):.2f}"
    )

    print(
        f"  Oraret me f(S)=0: "
        f"{scores.count(0)}"
    )

    show_histogram(scores)

    print(
        "  SHENIM: Rezultatet bazohen "
        "vetem ne mostren e analizuar."
    )

    # Analiza e fqinjesise
    print(
        "\n4. Fqinjesia e orarit "
        "(nderrimi i lojtareve)"
    )

    total_neighbors = (
        weeks
        * math.comb(groups, 2)
        * size * size
    )

    print(
        f"  Fqinje te mundshme per nje orar: "
        f"{total_neighbors}"
    )

    if total_neighbors == 0:
        print(
            "  Nuk ka dy grupe te ndryshme "
            "per te bere nderrim."
        )
        return

    counts = {
        "me mire": 0,
        "baraz": 0,
        "me keq": 0,
    }

    for _ in range(neighbor_schedules):

        schedule = random_schedule(
            groups, size, weeks, rng
        )

        base_score = objective(schedule)

        for _ in range(swaps_per_schedule):

            neighbor = random_neighbor(
                schedule, rng
            )

            other_score = objective(neighbor)

            if other_score < base_score:
                counts["me mire"] += 1

            elif other_score == base_score:
                counts["baraz"] += 1

            else:
                counts["me keq"] += 1

    tested_swaps = (
        neighbor_schedules * swaps_per_schedule
    )

    print(
        f"  Nderrime te testuara: "
        f"{tested_swaps}"
    )

    for label, count in counts.items():
        print(
            f"  {label.capitalize()}: "
            f"{count / tested_swaps:.1%}"
        )

    print(
        "  SHENIM: Perqindjet jane vleresime "
        "nga nderrime te rastësishme."
    )


# 6. Ekzekutimi i programit
def main():

    parser = argparse.ArgumentParser(
        description=(
            "Analiza e landscape "
            "per Social Golfers Problem"
        )
    )

    parser.add_argument(
        "--groups", type=int, default=8
    )

    parser.add_argument(
        "--size", type=int, default=4
    )

    parser.add_argument(
        "--weeks", type=int, default=10
    )

    parser.add_argument(
        "--samples", type=int, default=500
    )

    parser.add_argument(
        "--neighbor-schedules",
        type=int,
        default=5,
    )

    parser.add_argument(
        "--swaps-per-schedule",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--seed", type=int, default=42
    )

    args = parser.parse_args()

    if (
        args.groups < 1
        or args.size < 2
        or args.weeks < 1
    ):
        parser.error(
            "Groups dhe weeks duhet te jene >= 1; "
            "size duhet te jete >= 2."
        )

    if (
        args.samples < 1
        or args.neighbor_schedules < 1
        or args.swaps_per_schedule < 1
    ):
        parser.error(
            "Numri i mostrave dhe nderrimeve "
            "duhet te jete >= 1."
        )

    analyze(
        args.groups,
        args.size,
        args.weeks,
        args.samples,
        args.neighbor_schedules,
        args.swaps_per_schedule,
        args.seed,
    )


if __name__ == "__main__":
    main()
