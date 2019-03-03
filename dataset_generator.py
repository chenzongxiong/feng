import sys
import time
import argparse

import numpy as np
import trading_data as tdata
import log as logging
import constants
import colors

LOG = logging.getLogger(__name__)

methods = constants.METHODS
weights = constants.WEIGHTS
widths = constants.WIDTHS
NB_PLAYS = constants.NB_PLAYS
points = constants.POINTS
UNITS = constants.UNITS

def operator_generator():
    # states = [1, 4, 10 -1, -4, -10]
    states = [0]
    for method in methods:
        for weight in weights:
            for width in widths:
                inputs = []
                outputs = []
                for state in states:
                    LOG.debug("Processing method: {}, weight: {}, width: {}, state: {}".format(method, weight, width, state))
                    inputs_, outputs_ = tdata.DatasetGenerator.systhesis_operator_generator(points=points,
                                                                                            weight=weight,
                                                                                            width=width,
                                                                                            state=state,
                                                                                            with_noise=True)
                    inputs.append(inputs_)
                    outputs.append(outputs_)
                fname = constants.FNAME_FORMAT['operators'].format(method=method, weight=weight, width=width, points=points)
                inputs = np.hstack(inputs)
                outputs = np.hstack(outputs)
                outputs = outputs.T
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def play_generator():
    for method in methods:
        for weight in weights:
            for width in widths:
                LOG.debug("Processing method: {}, weight: {}, width: {}".format(method, weight, width))
                fname = constants.FNAME_FORMAT['operators'].format(method=method, weight=weight, width=width, points=points)
                try:
                    inputs, _ = tdata.DatasetLoader.load_data(fname)
                except FileNotFoundError:
                    inputs = None

                inputs, outputs = tdata.DatasetGenerator.systhesis_play_generator(points=points, inputs=inputs)
                fname = constants.FNAME_FORMAT['plays'].format(method=method, weight=weight, width=width, points=points)
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def model_generator(units=1, nb_plays=1):
    units = int(units)
    nb_plays = int(nb_plays)
    for method in methods:
        for weight in weights:
            for width in widths:
                LOG.debug("generate data for method {}, weight {}, width {}, units {}, nb_plays {}".format(
                    method, weight, width, units, nb_plays
                ))
                fname = constants.FNAME_FORMAT['plays'].format(method=method, weight=weight, width=width, points=points)
                try:
                    inputs, _ = tdata.DatasetLoader.load_data(fname)
                except FileNotFoundError:
                    inputs = None
                import time
                start = time.time()
                inputs, outputs = tdata.DatasetGenerator.systhesis_model_generator(nb_plays=nb_plays,
                                                                                   points=points,
                                                                                   units=units,
                                                                                   inputs=inputs)
                end = time.time()
                LOG.debug("time cost: {} s".format(end-start))

                fname = constants.FNAME_FORMAT['models'].format(method=method, weight=weight, width=width, nb_plays=nb_plays, units=units, points=points)
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def markov_chain(points, mu=0, sigma=0.001):
    points = int(points)
    mu = float(mu)
    sigma = float(sigma)
    B = tdata.DatasetGenerator.systhesis_markov_chain_generator(points, mu, sigma)
    fname = constants.FNAME_FORMAT['mc'].format(points=points, mu=mu, sigma=sigma)
    tdata.DatasetSaver.save_data(B, B, fname)


def operator_generator_with_noise():
    states = [0]
    mu = 0
    sigma = 0.1
    points = 5000

    for method in methods:
        for weight in weights:
            for width in widths:
                inputs = []
                outputs = []
                for state in states:
                    LOG.debug("Processing method: {}, weight: {}, width: {}, state: {}, mu: {}, sigma: {}, points: {}".format(method, weight, width, state, mu, sigma, points))

                    inputs_, outputs_ = tdata.DatasetGenerator.systhesis_operator_generator(points=points,
                                                                                            weight=weight,
                                                                                            width=width,
                                                                                            state=state,
                                                                                            with_noise=True,
                                                                                            mu=mu,
                                                                                            sigma=sigma)
                    inputs.append(inputs_)
                    outputs.append(outputs_)
                fname = constants.FNAME_FORMAT['operators_noise'].format(method=method, weight=weight, width=width, mu=mu, sigma=sigma, points=points)
                inputs = np.hstack(inputs)
                outputs = np.hstack(outputs)
                outputs = outputs.T
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def play_generator_with_noise():
    mu = 1
    sigma = 0.01
    for method in methods:
        for weight in weights:
            for width in widths:
                LOG.debug("Processing method: {}, weight: {}, width: {}".format(method, weight, width))
                fname = constants.FNAME_FORMAT['operators_noise'].format(method=method, weight=weight, width=width, mu=mu, sigma=sigma)
                try:
                    inputs, _ = tdata.DatasetLoader.load_data(fname)
                except FileNotFoundError:
                    inputs = None

                inputs, outputs = tdata.DatasetGenerator.systhesis_play_generator(points=points, inputs=inputs)
                fname = constants.FNAME_FORMAT['plays_noise'].format(method=method, weight=weight, width=width, mu=mu, sigma=sigma)
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def model_generator_with_noise():
    mu = 0
    sigma = 0.1
    points = 5000
    units = 20
    nb_plays = 40
    for method in methods:
        for weight in weights:
            for width in widths:
                LOG.debug("generate data for method {}, weight {}, width {}, units {}, nb_plays {}".format(
                    method, weight, width, units, nb_plays
                ))
                fname = constants.FNAME_FORMAT['operators_noise'].format(method=method, weight=weight, width=width, points=points, mu=mu, sigma=sigma)
                try:
                    inputs, _ = tdata.DatasetLoader.load_data(fname)
                except FileNotFoundError:
                    inputs = None

                import time
                start = time.time()
                inputs, outputs = tdata.DatasetGenerator.systhesis_model_generator(nb_plays=nb_plays,
                                                                                   points=points,
                                                                                   units=units,
                                                                                   inputs=inputs,
                                                                                   batch_size=1)
                end = time.time()
                LOG.debug("time cost: {} s".format(end-start))

                fname = constants.FNAME_FORMAT['models_noise'].format(method=method, weight=weight, width=width, nb_plays=nb_plays, units=units, points=points, mu=mu, sigma=sigma)
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def operator_noise_test_generator():
    states = [2]
    mu = 0
    sigma = 0.1
    points = 100
    methods = ["mixed"]

    for method in methods:
        for weight in weights:
            for width in widths:
                inputs = []
                outputs = []
                for state in states:
                    LOG.debug("Processing method: {}, weight: {}, width: {}, state: {}, mu: {}, sigma: {}, points: {}".format(method, weight, width, state, mu, sigma, points))

                    inputs_, outputs_ = tdata.DatasetGenerator.systhesis_operator_generator(points=points,
                                                                                            weight=weight,
                                                                                            width=width,
                                                                                            state=state,
                                                                                            with_noise=True,
                                                                                            mu=mu,
                                                                                            sigma=sigma,
                                                                                            method=method)
                    inputs.append(inputs_)
                    outputs.append(outputs_)
                fname = constants.FNAME_FORMAT['operators_noise_test'].format(method=method, weight=weight, width=width, mu=mu, sigma=sigma, points=points, state=state)
                inputs = np.hstack(inputs)
                outputs = np.hstack(outputs)
                outputs = outputs.T
                tdata.DatasetSaver.save_data(inputs, outputs, fname)


def model_noise_test_generator():
    mu = 0
    sigma = 0.1
    points = 5000
    nb_plays = 40
    state = 0

    units = 20
    methods = ["mixed"]
    for method in methods:
        for weight in weights:
            for width in widths:
                LOG.debug("generate data for method {}, weight {}, width {}, units {}, nb_plays {}".format(
                    method, weight, width, units, nb_plays
                ))
                fname = constants.FNAME_FORMAT['operators_noise_test'].format(method=method, weight=weight, width=width, points=points, mu=mu, sigma=sigma, state=state)
                try:
                    inputs, _ = tdata.DatasetLoader.load_data(fname)
                except FileNotFoundError:
                    inputs = None

                import time
                start = time.time()
                inputs, outputs = tdata.DatasetGenerator.systhesis_model_generator(nb_plays=nb_plays,
                                                                                   points=points,
                                                                                   units=units,
                                                                                   inputs=inputs,
                                                                                   batch_size=1)
                end = time.time()
                LOG.debug("time cost: {} s".format(end-start))

                fname = constants.FNAME_FORMAT['models_nb_plays_noise_test'].format(method=method, weight=weight, width=width, nb_plays=nb_plays, units=units, points=points, mu=mu, sigma=sigma, state=state)
                tdata.DatasetSaver.save_data(inputs, outputs, fname)



def model_nb_plays_generator_with_noise():
    mu = 0
    # sigma = 0.1
    # sigma = 0.001
    # sigma = 0.01
    # sigma = 0.001
    # sigma = 2
    sigma = 3
    points = 1000
    units = 20
    nb_plays = 20

    # method = 'sin'
    # method = 'mixed'
    method = 'noise'
    with_noise = False
    # diff_weights = False
    diff_weights = True

    run_test = True

    activation = 'tanh'
    # activation = None

    input_dim = 1
    state = 0


    if method == 'noise':
        with_noise = True
    if with_noise is False:
        mu = 0
        sigma = 0

    if diff_weights is True and run_test is True:
        file_key = 'models_diff_weights_test'
    elif diff_weights is True:
        file_key  = 'models_diff_weights'
    else:
        file_key = 'models'

    LOG.debug("generate model data for method {}, units {}, nb_plays {}, mu: {}, sigma: {}, points: {}, activation: {}, input_dim: {}".format(method, units, nb_plays, mu, sigma, points, activation, input_dim))

    inputs = None

    start = time.time()
    inputs, outputs = tdata.DatasetGenerator.systhesis_model_generator(inputs=inputs,
                                                                       nb_plays=nb_plays,
                                                                       points=points,
                                                                       units=units,
                                                                       mu=mu,
                                                                       sigma=sigma,
                                                                       input_dim=input_dim,
                                                                       activation=activation,
                                                                       with_noise=with_noise,
                                                                       method=method,
                                                                       diff_weights=diff_weights)
    end = time.time()
    LOG.debug("time cost: {} s".format(end-start))
    # if diff_weights is True:
    fname = constants.DATASET_PATH[file_key].format(method=method, activation=activation, state=state, mu=mu, sigma=sigma, units=units, nb_plays=nb_plays, points=points, input_dim=input_dim)
    # else:
    #     fname = constants.DATASET_PATH['models'].format(method=method, activation=activation, state=state, mu=mu, sigma=sigma, units=units, nb_plays=nb_plays, points=points, input_dim=input_dim)

    LOG.debug(colors.cyan("Write  data to file {}".format(fname)))
    tdata.DatasetSaver.save_data(inputs, outputs, fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--operator", dest="operator",
                        required=False,
                        action="store_true",
                        help="generate operators' dataset")
    parser.add_argument("--play", dest="play",
                        required=False,
                        action="store_true",
                        help="generate plays' dataset")
    parser.add_argument("--model", dest="model",
                        required=False,
                        action="store_true",
                        help="generate models' dataset")

    parser.add_argument("--nb_plays", dest="nb_plays",
                        required=False,
                        type=int)
    parser.add_argument("--units", dest="units",
                        required=False,
                        type=int)

    parser.add_argument("--GF", dest="GF",
                        required=False,
                        action="store_true",
                        help="generate G & F models' dataset")

    parser.add_argument("--operator-noise", dest="operator_noise",
                        required=False,
                        action="store_true",
                        help="generate operators' dataset")

    parser.add_argument("--play-noise", dest="play_noise",
                        required=False,
                        action="store_true",
                        help="generate plays' dataset")

    parser.add_argument("--mc", dest="mc",
                        required=False,
                        action="store_true")
    parser.add_argument("--mu", dest="mu",
                        required=False,
                        type=float)

    parser.add_argument("--sigma", dest="sigma",
                        required=False,
                        type=float)
    parser.add_argument("--points", dest="points",
                        required=False,
                        type=int)


    parser.add_argument("--model-noise", dest="model_noise",
                        required=False,
                        action="store_true",
                        help="generate plays' dataset")

    argv = parser.parse_args(sys.argv[1:])

    if argv.operator:
        operator_generator()
    if argv.play:
        play_generator()
    if argv.model:
        model_generator(argv.units, argv.nb_plays)
    if argv.GF:
        GF_generator()
    if argv.operator_noise:
        # operator_generator_with_noise()
        operator_noise_test_generator()
    if argv.play_noise:
        play_generator_with_noise()
    if argv.mc:
        markov_chain(argv.points, argv.mu, argv.sigma)
    if argv.model_noise:
        # model_generator_with_noise()
        # model_noise_test_generator()
        model_nb_plays_generator_with_noise()
