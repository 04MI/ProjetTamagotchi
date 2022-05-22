import unittest
from tamagotchi import Tamagotchi

DAY = 30*60*60*24

class TamagotchiTest(unittest.TestCase):

    def test_tamagotchi_init_ShouldInitWithMinimalGivenParameters(self):
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0


        test = Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)
        self.assertIsInstance(test, Tamagotchi)
        self.assertEqual(test.name, name)
        self.assertEqual(test.health, health)
        self.assertEqual(test.gender, gender)
        self.assertEqual(test.hunger, hunger)
        self.assertEqual(test.happiness, happiness)
        self.assertEqual(test.sickness, sickness)
        self.assertEqual(test.lifetime, lifetime)

    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_tamagotchi_updateEvolution_ShouldEvolveAsBaby(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.lifetime = 0
        test.updateEvolution()

        self.assertEqual(test.evolution['name'], "bébé")

    def test_tamagotchi_updateEvolution_ShouldInitAsChild(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.lifetime = DAY*2
        test.updateEvolution()

        self.assertEqual(test.evolution['name'], "enfant")
    
    def test_tamagotchi_updateEvolution_ShouldInitAsAdult(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.lifetime = DAY*3
        test.updateEvolution()

        self.assertEqual(test.evolution['name'], "adulte")

    def test_tamagotchi_updateEvolution_ShouldInitAsElder(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.lifetime = DAY*4
        test.updateEvolution()

        self.assertEqual(test.evolution['name'], "vieux")

    def test_tamagotchi_isSick_ShouldReturnNotSick(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.sickness = 0
        ret = test.isSick()

        self.assertFalse(ret)

    def test_tamagotchi_isSick_ShouldReturnSick(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.sickness = 10
        ret = test.isSick()

        self.assertTrue(ret)

    def test_tamagotchi_isDead_ShouldReturnFalseIfHealthGreaterThanZero(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.health = 10
        ret = test.isDead()

        self.assertFalse(ret)
    
    def test_tamagotchi_isDead_ShouldReturnTrueIfHealthLessThanZero(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.health = -10
        ret = test.isDead()

        self.assertTrue(ret)
    
    def test_tamagotchi_isDead_ShouldReturnFalseIfHealthEqualToZero(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.health = 0
        ret = test.isDead()

        self.assertTrue(ret)
    
    def test_tamagotchi_activity_healing_ShouldSetSicknessToZero(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.sickness = 1337
        test.activity_healing()

        self.assertEqual(test.sickness, 0)

    def test_tamagotchi_activity_feeding_ShouldDecreaseHungerByPredifinedValue(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.hunger = 100
        test.activity_feeding()

        self.assertTrue(test.hunger < 100)

    def test_tamagotchi_activity_feeding_ShouldNotUnderFlowHungerValue(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.hunger = 0
        test.activity_feeding()

        self.assertTrue(test.hunger == 0)
    
    def test_tamagotchi_activity_feeding_ShouldIncreaseHappiness(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.hunger = 0
        test.happiness = 50
        old = test.happiness
        test.activity_feeding()

        self.assertTrue(test.happiness > old)

    def test_tamagotchi_activity_feeding_ShouldNotOverflowHappinessValue(self):
        test = TamagotchiTest.initMinimalTamagotchi()
        test.hunger = 0
        test.happiness = 100
        test.activity_feeding()

        self.assertTrue(test.happiness == 100)
    
    def test_addFriend_ShouldAddTheFriendToTheFriendlist(self):
        friend = {'name':'testFriend'}
        test = TamagotchiTest.initMinimalTamagotchi()
        
        test.addFriend(friend)

        self.assertEqual(1, len(test.friends))
        self.assertEqual(friend, test.friends[0])

    def test_addFriend_ShouldNotAddTheSameFriendTwiceToTheFriendlist(self):
        friend = {'name':'testFriend'}
        test = TamagotchiTest.initMinimalTamagotchi()
        
        test.addFriend(friend)
        test.addFriend(friend)

        self.assertEqual(1, len(test.friends))
        self.assertEqual(friend, test.friends[0])

    def test_tamagotchi_updateHunger_ShouldIncreaseHungerAccordingToModifier(self): 
        test = TamagotchiTest.initMinimalTamagotchi()
        test.hunger = 0
        test.updateHunger()

        self.assertEqual(test.hunger, 0.02)

    def test_tamagotchi_updateHunger_ShouldFallSickIfTooHungry(self): 
        test = TamagotchiTest.initMinimalTamagotchi()
        test.hunger = 51
        test.sickness = 0
        test.happiness = 0.04
        test.updateHunger()

        self.assertTrue(test.isSick())
        self.assertEqual(test.sickness, 0.002)
        self.assertEqual(test.happiness, 0.02)
    
    def test_tamagotchi_updateSickness_ShouldDecreaseHealth(self):
        # expected formula : health = health - ((sickness + SICKNESS_MODIFIER) * 0.01)
        test = TamagotchiTest.initMinimalTamagotchi()
        test.sickness = 0.002

        control = test.health - ((test.sickness + 0.002) * 0.01)

        test.updateSickness()

        self.assertEqual(test.health, control)

    def test_tamagotchi_updateSickness_ShouldNotDecreaseHealth(self):
        # expected formula : health = health - ((sickness + SICKNESS_MODIFIER) * 0.01)
        test = TamagotchiTest.initMinimalTamagotchi()
        test.sickness = 0
        test.updateSickness()
        self.assertEqual(test.health, 100)