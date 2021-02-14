import argparse


def get_parser(sysArgs):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pid", help="PID of the MU instance", type=int)
    parser.add_argument(
        "--test",
        help="For testing the PID. If true, mu window will get focused",
        type=str_to_bool)
    parser.add_argument(
        "--party-members",
        help="Number of members in party, default 0 (no party)",
        default=0, type=int)
    parser.add_argument(
        "--party-buffs",
        help="Number of the buff skills for party (default 1, 2, 3)",
        nargs="+", default=[1, 2, 3],
        type=int)
    parser.add_argument(
        "--heal-buff", help="Number of the healing buff (default 3)",
        default=3, type=int)
    parser.add_argument(
        "--must-heal",
        help="Trigger healing buff or not (default True)",
        default=True, type=str_to_bool)
    parser.add_argument(
        "--click",
        help="Mouse click to simulate (right, left, middle)",
        type=str)
    parser.add_argument(
        "--click-delay", help="Mouse click delay", default=0.5,
        type=float, required="--click" in sysArgs)
    parser.add_argument(
        "--click-skill-delay",
        help="Delay of party buffs if clicker is on", default=0,
        type=float)
    parser.add_argument(
        "--click-skill-default",
        help="Default skill to use for clicker", type=int)

    return parser


def normalize_args(sysArgs):
    new_args = []
    for a in sysArgs:
        if a.find("=") >= 0:
            a = a.split("=")
            new_args = new_args + a
        else:
            new_args = new_args + [a]

    return new_args


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')
