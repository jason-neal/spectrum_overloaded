"""Differential Class which takes the difference between two spectra."""
from spectrum_overload.Spectrum import Spectrum
# Begin Feburary 2017
# Jason Neal

# TODO: Add in s-profile from
# Ferluga 1997: Separating the spectra of binary stars-I. A simple method: Secondary reconstruction

class DifferentialSpectrum(object):
    """A differential spectrum."""

        def check_compatibility(spec1, spec2):
            """Check spectra are compatible to take differences.

            Requires most of the setting to be the same. Have included a CRIRES only parameters also.
            """
            compatible = True
            for check in ["EXPTIME", "HIERARCH ESO INS SLIT1 WID", "OBJECT"]:
                if spec1.header[check] != spec1.header[check]:
                    print("The Spectral property '{}' are not compatible. {}, {}".format(check, spec1.header[check], spec2.header[check]))
                    compatible = False
            return compatible

    def __init__(self, Spectrum1, Spectrum2, params=None):
        """Initalise lass with both spectra."""
        if not(Spectrum1.calibrated and Spectrum2.calibrated):
            raise ValueError("Input spectra are not calibrated.")

        if check_compatibility(spec1, spec2):
            self.spec1 = Spectrum1
            self.spec2 = Spectrum2
            self.diff = None
        else:
            raise ValueError("The spectra are not compatible.")

    def barycentric_correct(self):
        """Barycentic correct each spectra."""
        pass

    def rest_frame(self, frame):
        """Change restframe to one of the spectra."""
        pass

    def diff(self):
        """Calculate difference between the two spectra."""
        if check_compatibility(self.spec1, self.spec2):
            return self.spec1 - self.spec2
        else:
            raise ValueError("The spectra are not compatible.")
        # TODO: Access interpolations

    def sort(self, method="time"):
        """Sort spectra in specific order. e.g. time, reversed."""
        pass

    def swap(self):
        """Swap order of the two spectra."""
        self.spec1, self.spec2 = self.spec2, self.spec1

    def add_orbital_params(self, params):
        """A dictionary of orbital parameters to use for shifting frames."""
        self.params = params
