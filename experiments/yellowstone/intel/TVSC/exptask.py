'''test'''

from vt_setup import VecExp

# goals of the TVSC tests
# - why the code modifications based on Vector Advisor's recommendation does not improve vectorization and/or performance?
# - collect current status
# - select target loops for vectorization
# - use Intel Vectorization Advisor for its recommendations
# - try to apply the recommendations
# - summrize the result

class MyExp2(VecExp):
    def set_actions(self):
        return ["export EXP=111"]

class MyExp(VecExp):
    def set_actions(self):
        # generate a shell script
        # execute the shell script
        # cleanup if necessary
        return [ "echo EXP $EXP", ( self.myexp, None, None ) ]

    def set_setup(self):
        return [ MyExp2.EXPID ]

    def myexp(self):
        print('TEST CUSTOMIZED: %s'%MyExp2.EXPID)
