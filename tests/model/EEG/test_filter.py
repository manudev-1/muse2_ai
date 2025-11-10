import pytest
import numpy as np

from model.EEG.Filter import Filter

class TestFilter:

    @pytest.mark.parametrize(
        "data, low, high, fs, order, expected_shape",
        [
            (
                np.sin(2 * np.pi * 10 * np.linspace(0, 1, 1000)),
                5,
                15,
                1000,
                5,
                (1000,)
            ),
            (
                np.sin(2 * np.pi * 5 * np.linspace(0, 1, 500)) + 
                np.sin(2 * np.pi * 20 * np.linspace(0, 1, 500)),
                10,
                30,
                500,
                4,
                (500,)
            ),
            (
                np.random.randn(1000),
                1,
                40,
                200,
                3,
                (1000,)
            ),
            (
                np.sin(2 * np.pi * 15 * np.linspace(0, 1, 800)),
                10,
                20,
                800,
                2,
                (800,)
            ),
        ]
    )
    def test_bandpass_filter(self, data, low, high, fs, order, expected_shape):
        result = Filter.bandpass_filter(data, low, high, fs, order)
        
        assert result.shape == expected_shape
        assert isinstance(result, np.ndarray)
        
        assert not np.any(np.isnan(result))
        assert not np.any(np.isinf(result))

    @pytest.mark.parametrize(
        "signal, fs, f0, Q, expected_shape",
        [
            (
                np.random.randn(1000) + 0.5 * np.sin(2 * np.pi * 50 * np.linspace(0, 1, 1000)),
                256,
                50.0,
                30.0,
                (1000,)
            ),
            (
                np.random.randn(800) + 0.3 * np.sin(2 * np.pi * 60 * np.linspace(0, 1, 800)),
                200,
                60.0,
                25.0,
                (800,)
            ),
            (
                np.sin(2 * np.pi * 50 * np.linspace(0, 1, 600)),
                256,
                50.0,
                50.0,
                (600,)
            ),
            (
                np.random.randn(1200) + 0.4 * np.cos(2 * np.pi * 60 * np.linspace(0, 1, 1200)),
                500,
                60.0,
                30.0,
                (1200,)
            ),
        ]
    )
    def test_notch_filter(self, signal, fs, f0, Q, expected_shape):
        result = Filter.notch_filter(signal, fs, f0, Q)

        assert result.shape == expected_shape
        assert isinstance(result, np.ndarray)

        assert not np.any(np.isnan(result))
        assert not np.any(np.isinf(result))

    @pytest.mark.parametrize(
        "signal, threshold, expected",
        [
            (np.array([1.0, 2.0, 3.0, -2.0]), 150.0, True),
            (np.zeros(100), 150.0, True),
            (np.ones(50) * 100.0, 150.0, True),
            (np.array([-149.0, 149.0, 0.0]), 150.0, True),
            (np.array([1.0, 200.0, 3.0]), 150.0, False),
            (np.array([-160.0, 10.0, 20.0]), 150.0, False),
            (np.ones(10) * 200.0, 150.0, False),
            (np.array([149.0, 150.0, 149.0]), 150.0, False),
        ]
    )
    def test_is_clean(self, signal, threshold, expected):
        result = Filter.is_clean(signal, threshold)

        assert result == expected