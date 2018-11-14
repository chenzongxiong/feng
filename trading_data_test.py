import trading_data
import log as logging


LOG = logging.getLogger(__name__)


if __name__ == "__main__":
    points = 5
    inputs, outputs = trading_data.DatasetGenerator.systhesis_play_operator_generator(points)
    inputs, outputs = trading_data.DatasetGenerator.systhesis_play_generator(points)
    nb_plays = 3
    inputs, outputs, plays_outputs = trading_data.DatasetGenerator.systhesis_model_generator(nb_plays, points, debug_plays=True)
    LOG.debug("inputs.shape: {}, outputs.shape: {}, plays_outputs.shape: {}".format(inputs.shape, outputs.shape, plays_outputs.shape))

    fname = "./training-data/players/sin-2-5-4-tanh.csv"
    inputs, outputs = trading_data.DatasetLoader.load_data(fname)
    train_inputs, train_outputs = trading_data.DatasetLoader.load_train_data(fname)
    test_inputs, test_outputs = trading_data.DatasetLoader.load_test_data(fname)

    fname = "./training-data/players/sin-2-5-4-tanh.csv.bk"
    trading_data.DatasetSaver.save_data(inputs, outputs, fname)
