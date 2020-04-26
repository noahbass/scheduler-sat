# scheduler-sat

[![CI Status](https://github.com/noahbass/scheduler-sat/workflows/ci/badge.svg)](https://github.com/noahbass/scheduler-sat/actions?query=workflow%3Aci)
[![MIT license](https://img.shields.io/github/license/noahbass/scheduler-sat.svg)](http://opensource.org/licenses/MIT)

> Using a SAT solver to prove correctness of schedules given a list of constraints.

## Quick Start

This project includes both Python and BDDs (for a SAT solver).

### Python code

Requirements:

- Python 3 (and pip 3)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional)

Clone and run tests:

```sh
$ git clone git@github.com:noahbass/scheduler-sat.git
$ cd scheduler-sat
$ pip3 install -r requirements.txt # optionally use virtualenv before this step
$ python3 main.test.py -v
```

### SAT code

Requirements:

- [sbsat](http://gauss.ececs.uc.edu/franco_files/sbsat.html)

Clone and run:

```sh
$ git clone git@github.com:noahbass/scheduler-sat.git
$ cd scheduler-sat
$ sbsat validator.bdd # or use ./sbsat.run validator.bdd
# Reading File validator.bdd  ....
# Reading ITE ... Done
# Preprocessing .... Done                            
# Satisfiable
# Total Time: 0.005
```

## Presentation

[Slide deck](https://docs.google.com/presentation/d/1xzLT3W-2BYiKr6U1CkECqEIgpgrT6bFV3VBb8qw0oyE/edit?usp=sharing)

## Python Tests

```sh
$ pip3 install -r requirements.txt
$ python3 main.test.py -v
$ python3 validator.test.py -v
```

## Authors

[@noahbass](https://github.com/noahbass) and [@linkb98](https://github.com/linkb98)

## License

[MIT](LICENSE)
