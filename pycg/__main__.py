import argparse
import json

from pycg import formats
from pycg.pycg import CallGraphGenerator
from pycg.utils.constants import CALL_GRAPH_OP, KEY_ERR_OP


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entry_point", nargs="*", help="Entry points to be processed")
    parser.add_argument(
        "--package", help="Package containing the code to be analyzed", default=None
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        help=(
            "Maximum number of iterations through source code. "
            "If not specified a fix-point iteration will be performed."
        ),
        default=-1,
    )
    parser.add_argument(
        "--operation",
        type=str,
        choices=[CALL_GRAPH_OP, KEY_ERR_OP],
        help=(
            "Operation to perform. Choose "
            + CALL_GRAPH_OP
            + " for call graph generation (default) or "
            + KEY_ERR_OP
            + " for key error detection on dictionaries."
        ),
        default=CALL_GRAPH_OP,
    )

    parser.add_argument(
        "--as-graph-output", help="Output for the assignment graph", default=None
    )
    parser.add_argument("-o", "--output", help="Output path", default=None)

    args = parser.parse_args()

    cg = CallGraphGenerator(
        args.entry_point, args.package, args.max_iter, args.operation
    )
    cg.analyze()

    if args.operation == CALL_GRAPH_OP:
        formatter = formats.Simple(cg)
        output = formatter.generate()
    else:
        output = cg.output_key_errs()

    as_formatter = formats.AsGraph(cg)

    if args.output:
        with open(args.output, "w+") as f:
            f.write(json.dumps(output))
    else:
        print(json.dumps(output))

    if args.as_graph_output:
        with open(args.as_graph_output, "w+") as f:
            f.write(json.dumps(as_formatter.generate()))


if __name__ == "__main__":
    main()
