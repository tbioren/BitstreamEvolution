import subprocess
import time
from Circuit.DirectRouting.simulation import generate_asc_config, make_individual

num_tests = 1_000_000
asc_path = "temp.asc"

if __name__ == "__main__":
    successes = 0
    failures = 0
    start_time = time.time()

    for i in range(num_tests):
        circuit = make_individual(35)
        with open(asc_path, "w") as f:
            f.write(generate_asc_config(circuit))

        result = subprocess.run(
            ["icepack", asc_path, "temp.bin"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            successes += 1
        else:
            failures += 1

        if (i + 1) % 1000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            print(f"Progress: {i + 1}/{num_tests} ({rate:.1f} iter/s) | "
                  f"pass={successes} fail={failures}", flush=True)

    elapsed = time.time() - start_time

    print("\n" + "=" * 40)
    print("ICEPACK RUN REPORT")
    print("=" * 40)
    print(f"Total tests:  {num_tests:>10,}")
    print(f"Successes:    {successes:>10,}  ({100*successes/num_tests:.2f}%)")
    print(f"Failures:     {failures:>10,}  ({100*failures/num_tests:.2f}%)")
    print(f"Elapsed time: {elapsed:>10.1f}s  ({num_tests/elapsed:.1f} iter/s)")
    print("=" * 40)