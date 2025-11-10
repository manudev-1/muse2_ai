import pytest
import numpy as np

from model.EEG.Band import Band

class TestBand:

    @pytest.mark.parametrize(
        "freqs, psd, expected_bands, description",
        [
            (
                np.linspace(0, 60, 1000),
                np.ones(1000),
                ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
                "Costant PSD on all the bands"
            ),
            (
                np.linspace(0, 60, 1000),
                np.exp(-(np.linspace(0, 60, 1000) - 10)**2),
                ['Alpha'],
                "Peak in the Alpha band"
            ),
            (
                np.linspace(30, 50, 500),
                np.ones(500),
                ['Gamma'],
                "Only Gamma band present"
            ),
            (
                np.linspace(0, 60, 100),
                np.zeros(100),
                ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
                "Zero PSD in all bands"
            ),
            (
                np.linspace(0, 10, 200),
                np.ones(200),
                ['Delta', 'Theta', 'Alpha'],
                "Frequencies only in the low bands"
            ),
        ]
    )
    def test_compute_bandpower(self, freqs, psd, expected_bands, description):
        bands = {
            'Delta': (0.5, 4),
            'Theta': (4, 8),
            'Alpha': (8, 12),
            'Beta': (12, 30),
            'Gamma': (30, 50)
        }

        result = Band.compute_bandpower(freqs, psd)
        assert set(result.keys()) == set(bands.keys())
        
        for band_name, power in result.items():
            assert isinstance(power, float)
            assert not np.isnan(power)
            assert not np.isinf(power)
            
            if band_name in expected_bands and "zero" not in description.lower():
                assert power > 0
            elif "zero" in description.lower():
                assert power == 0.0