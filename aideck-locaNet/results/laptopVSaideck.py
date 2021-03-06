import matplotlib.pyplot as plt
import numpy as np

conf_maps_laptop = np.array([
[-17,-20,-20,-20,-18,-17,-24,-25,-22,-20,-20,-20,-20,-20,-20,-20,-20,-19,-18,-19,-20,-20,-20,-20,-20,-20,-21,-21,-21,-21,-22,-22,-22,-21,-21,-23,-25,-26,-24,-30],
[-19,-21,-21,-20,-20,-17,-16,-24,-24,-25,-22,-22,-22,-22,-21,-21,-21,-21,-21,-21,-21,-21,-22,-22,-22,-22,-22,-22,-22,-22,-23,-24,-25,-24,-24,-23,-24,-24,-25,-38],
[-16,-14,-15,-16,-17,-16,-16,-18,-22,-21,-22,-20,-19,-18,-19,-19,-20,-20,-19,-20,-21,-21,-21,-21,-21,-22,-22,-22,-21,-22,-23,-24,-24,-23,-22,-23,-23,-25,-26,-34],
[-16,-15,-15,-15,-16,-18,-16,-15,-21,-19,-18,-17,-18,-18,-19,-19,-20,-20,-19,-20,-20,-21,-21,-21,-21,-21,-21,-21,-21,-21,-21,-22,-23,-23,-22,-22,-22,-24,-26,-34],
[-17,-15,-15,-15,-16,-16,-17,-17,-18,-23,-21,-16,-17,-18,-19,-20,-20,-20,-20,-20,-20,-20,-21,-22,-21,-21,-21,-20,-20,-20,-20,-21,-22,-22,-22,-22,-22,-22,-26,-36],
[-17,-16,-16,-16,-16,-16,-16,-18,-19,-19,-21,-15,-17,-18,-19,-20,-20,-20,-20,-20,-20,-16,-18,-18,-19,-21,-21,-20,-19,-18,-19,-20,-21,-21,-21,-22,-21,-22,-23,-34],
[-18,-17,-17,-16,-17,-17,-17,-18,-18,-20,-22,-16,-17,-18,-19,-20,-20,-20,-20,-20,-18,-11,-14,-12,-16,-21,-21,-20,-19,-18,-19,-19,-21,-20,-21,-21,-21,-21,-23,-34],
[-19,-20,-18,-18,-17,-17,-18,-19,-18,-20,-21,-16,-17,-18,-19,-20,-20,-20,-20,-20,-18,-14,-14,-16,-19,-21,-20,-20,-20,-19,-19,-20,-20,-20,-21,-21,-21,-21,-21,-33],
[-17,-18,-19,-19,-18,-17,-18,-19,-19,-22,-22,-16,-17,-18,-19,-19,-20,-21,-20,-20,-22,-22,-15,-15,-20,-21,-21,-21,-20,-20,-20,-20,-21,-20,-20,-20,-21,-21,-21,-32],
[-13,-13,-15,-15,-16,-17,-19,-18,-20,-23,-24,-16,-17,-18,-18,-19,-20,-20,-21,-21,-21,-20,-20,-20,-20,-21,-21,-21,-21,-21,-21,-20,-20,-20,-20,-21,-21,-21,-22,-31],
[-17,-16,-13,-12,-14,-16,-19,-18,-19,-23,-23,-17,-18,-18,-18,-19,-19,-17,-18,-18,-18,-20,-20,-21,-17,-17,-19,-20,-21,-21,-20,-20,-20,-20,-20,-20,-20,-20,-22,-31],
[-17,-16,-19,-21,-20,-18,-17,-16,-19,-23,-24,-16,-17,-17,-18,-19,-18,-13,-16,-14,-15,-20,-21,-21,-15,-16,-14,-14,-18,-21,-20,-20,-20,-20,-19,-20,-20,-19,-21,-32],
[-19,-17,-18,-18,-19,-17,-13,-12,-15,-13,-15,-15,-17,-17,-18,-19,-16,-14,-12,-14,-17,-20,-21,-21,-17,-13,-14,-16,-19,-20,-20,-20,-20,-20,-19,-19,-19,-18,-21,-30],
[-16,-19,-12,-12,-13,-10,-9,-12,-10,-12,-12,-13,-18,-18,-18,-19,-21,-20,-14,-15,-19,-21,-21,-21,-21,-19,-14,-16,-20,-20,-20,-20,-19,-20,-19,-18,-14,-18,-19,-27],
[-13,-14,-15,-14,-11,-9,-9,-9,-12,-15,-12,-14,-18,-18,-18,-19,-19,-20,-20,-20,-20,-21,-21,-21,-22,-21,-20,-20,-22,-23,-22,-21,-20,-19,-19,-16,-15,-17,-18,-24],
[-20,-18,-15,-14,-12,-14,-15,-19,-18,-15,-16,-16,-18,-18,-18,-18,-19,-19,-19,-20,-20,-21,-21,-21,-21,-20,-13,-11,-14,-14,-16,-18,-17,-19,-19,-17,-16,-16,-20,-21],
[-22,-22,-21,-19,-15,-12,-12,-14,-16,-17,-18,-18,-18,-18,-18,-18,-19,-19,-18,-18,-19,-20,-21,-22,-22,-20,-9,-6,-5,-5,-4,-7,-16,-18,-18,-19,-20,-18,-15,-21],
[-23,-23,-21,-20,-19,-18,-17,-17,-17,-17,-18,-18,-18,-18,-18,-18,-18,-18,-16,-13,-11,-11,-11,-15,-19,-19,-16,-9,-6,-7,-8,-9,-18,-18,-19,-24,-23,-18,-15,-21],
[-23,-23,-21,-20,-19,-19,-19,-19,-18,-18,-18,-18,-18,-18,-18,-18,-18,-18,-15,-17,-18,-19,-19,-17,-21,-17,-19,-15,-10,-8,-10,-14,-18,-19,-19,-21,-21,-17,-16,-22],
[-24,-24,-22,-21,-20,-19,-19,-19,-17,-17,-17,-17,-18,-18,-18,-17,-18,-17,-15,-19,-21,-24,-23,-18,-21,-19,-18,-18,-18,-18,-18,-18,-18,-19,-20,-24,-21,-17,-16,-22],
[-25,-27,-23,-22,-21,-21,-19,-19,-18,-20,-18,-17,-18,-18,-18,-18,-18,-17,-18,-20,-17,-17,-19,-18,-21,-19,-18,-18,-18,-18,-18,-18,-19,-19,-22,-23,-21,-17,-16,-22],
[-26,-28,-25,-23,-22,-22,-23,-21,-24,-21,-21,-24,-25,-25,-25,-25,-25,-25,-25,-24,-20,-19,-17,-19,-23,-20,-18,-18,-18,-19,-19,-20,-21,-22,-24,-26,-24,-17,-16,-22],
[-26,-29,-27,-26,-22,-22,-22,-22,-21,-22,-26,-24,-25,-25,-25,-25,-24,-26,-28,-27,-23,-23,-24,-25,-29,-25,-23,-22,-23,-24,-25,-26,-26,-26,-28,-29,-23,-18,-16,-22],
[-25,-27,-25,-22,-21,-20,-22,-23,-15,-13,-18,-21,-19,-17,-18,-17,-17,-17,-18,-19,-22,-21,-16,-16,-22,-22,-24,-24,-25,-26,-25,-25,-24,-24,-22,-19,-20,-17,-15,-22],
[-16,-21,-20,-21,-23,-17,-18,-21,-19,-18,-22,-25,-26,-24,-24,-22,-21,-19,-15,-14,-16,-18,-19,-18,-22,-22,-22,-22,-21,-23,-23,-22,-22,-21,-19,-16,-16,-15,-17,-23],
[-15,-23,-22,-21,-20,-20,-19,-18,-18,-18,-19,-18,-19,-17,-18,-18,-19,-19,-19,-19,-19,-19,-20,-21,-25,-27,-26,-28,-28,-28,-27,-26,-28,-27,-25,-25,-22,-19,-19,-26],
[-16,-19,-21,-22,-22,-22,-24,-26,-27,-28,-28,-27,-29,-29,-28,-26,-28,-29,-29,-28,-28,-28,-27,-28,-29,-29,-29,-29,-29,-29,-27,-25,-25,-26,-28,-28,-27,-27,-22,-27],
[-17,-19,-21,-21,-22,-22,-22,-22,-22,-21,-21,-20,-20,-20,-19,-19,-19,-18,-18,-18,-20,-21,-20,-20,-19,-19,-19,-17,-18,-20,-21,-21,-21,-22,-21,-21,-23,-23,-22,-30]])

conf_maps_aideck = np.array([
[-18,-22,-22,-22,-20,-19,-24,-25,-23,-23,-21,-19,-21,-19,-19,-20,-20,-20,-19,-20,-20,-20,-21,-21,-21,-21,-21,-21,-21,-21,-21,-22,-22,-23,-25,-26,-25,-27,-24,-29],
[-19,-22,-22,-22,-21,-18,-18,-26,-24,-26,-24,-23,-22,-21,-21,-22,-21,-23,-22,-22,-22,-23,-24,-23,-23,-22,-23,-22,-23,-21,-24,-24,-26,-23,-24,-24,-25,-24,-26,-39],
[-15,-14,-17,-17,-17,-17,-18,-19,-23,-19,-20,-19,-16,-16,-18,-18,-20,-21,-19,-20,-21,-21,-22,-22,-21,-22,-22,-22,-22,-21,-22,-22,-23,-23,-21,-23,-25,-27,-26,-34],
[-16,-15,-16,-15,-17,-19,-18,-17,-22,-18,-16,-15,-15,-16,-19,-19,-21,-21,-18,-19,-20,-21,-22,-22,-21,-22,-22,-21,-21,-22,-24,-23,-24,-23,-21,-22,-24,-25,-27,-34],
[-16,-15,-16,-16,-16,-17,-18,-19,-19,-23,-21,-12,-14,-18,-18,-20,-21,-21,-21,-20,-20,-20,-20,-22,-22,-22,-22,-21,-22,-21,-21,-22,-22,-22,-22,-18,-20,-19,-27,-36],
[-17,-16,-16,-15,-15,-15,-17,-19,-21,-21,-20,-15,-15,-17,-19,-19,-21,-22,-22,-21,-21,-16,-19,-17,-19,-22,-22,-20,-18,-19,-20,-21,-21,-20,-19,-20,-19,-20,-24,-35],
[-19,-17,-17,-17,-17,-17,-17,-18,-19,-22,-24,-14,-14,-17,-19,-20,-21,-22,-22,-22,-19,-12,-14,-12,-15,-22,-22,-20,-18,-17,-18,-18,-19,-21,-19,-19,-20,-20,-22,-35],
[-20,-19,-19,-18,-18,-17,-18,-18,-20,-21,-21,-13,-14,-17,-17,-19,-21,-22,-22,-22,-20,-15,-15,-17,-19,-22,-22,-21,-20,-19,-19,-19,-19,-20,-18,-19,-17,-19,-22,-34],
[-18,-19,-19,-18,-19,-19,-19,-19,-18,-22,-22,-15,-14,-17,-18,-19,-20,-22,-22,-22,-22,-22,-18,-15,-21,-22,-22,-22,-21,-21,-20,-22,-21,-20,-19,-17,-19,-20,-21,-32],
[-12,-13,-14,-15,-17,-19,-18,-18,-19,-23,-24,-13,-14,-15,-18,-19,-20,-21,-22,-23,-22,-22,-22,-21,-20,-21,-21,-22,-22,-21,-19,-18,-20,-20,-18,-17,-19,-18,-20,-31],
[-17,-15,-14,-12,-14,-16,-18,-17,-18,-23,-22,-15,-16,-17,-18,-19,-19,-17,-18,-18,-18,-22,-22,-22,-17,-17,-19,-19,-21,-20,-20,-21,-20,-20,-19,-17,-18,-17,-20,-30],
[-17,-20,-20,-20,-19,-17,-17,-15,-18,-23,-23,-14,-14,-15,-18,-18,-16,-14,-16,-14,-14,-21,-22,-21,-15,-16,-15,-14,-17,-19,-20,-20,-20,-20,-18,-18,-18,-17,-20,-32],
[-20,-18,-20,-19,-20,-18,-13,-13,-15,-14,-14,-13,-16,-16,-17,-17,-16,-14,-13,-17,-17,-21,-22,-22,-17,-13,-13,-15,-18,-20,-20,-18,-20,-20,-18,-17,-17,-17,-22,-31],
[-16,-20,-13,-13,-13,-10,-7,-10,-11,-12,-10,-11,-16,-14,-16,-18,-19,-19,-15,-15,-20,-21,-22,-22,-21,-20,-14,-16,-18,-20,-20,-19,-20,-19,-18,-17,-13,-18,-19,-28],
[-14,-13,-14,-15,-10,-8,-9,-8,-11,-14,-11,-13,-15,-14,-18,-18,-19,-21,-20,-20,-20,-22,-22,-22,-22,-21,-18,-20,-22,-23,-20,-21,-20,-18,-17,-14,-16,-17,-20,-25],
[-19,-18,-13,-13,-12,-15,-17,-17,-17,-15,-14,-15,-16,-15,-16,-18,-19,-18,-18,-19,-21,-21,-22,-21,-20,-18,-13,-11,-14,-14,-17,-19,-16,-18,-17,-20,-17,-15,-19,-22],
[-22,-21,-18,-16,-14,-11,-13,-12,-15,-16,-17,-18,-17,-16,-17,-19,-18,-20,-18,-18,-19,-19,-21,-21,-20,-19,-8,-4,-4,-5,-5,-7,-15,-17,-17,-18,-19,-17,-14,-22],
[-24,-22,-20,-20,-18,-16,-15,-17,-17,-16,-17,-16,-17,-16,-16,-15,-15,-15,-14,-10,-9,-11,-11,-14,-18,-18,-14,-8,-7,-6,-7,-9,-16,-17,-20,-26,-25,-18,-15,-20],
[-25,-25,-21,-19,-19,-18,-15,-16,-15,-15,-15,-17,-15,-16,-17,-16,-15,-15,-12,-15,-17,-20,-18,-16,-19,-14,-16,-13,-9,-8,-9,-13,-17,-17,-18,-23,-23,-18,-16,-24],
[-26,-27,-23,-23,-19,-19,-17,-16,-14,-15,-15,-14,-16,-16,-16,-16,-18,-16,-15,-16,-21,-25,-23,-18,-22,-17,-17,-16,-17,-16,-16,-17,-18,-18,-19,-25,-23,-20,-17,-24],
[-28,-30,-26,-24,-19,-17,-17,-19,-19,-19,-18,-15,-16,-17,-16,-17,-17,-18,-19,-19,-17,-16,-19,-18,-19,-18,-18,-17,-19,-18,-16,-17,-19,-21,-22,-24,-22,-18,-17,-23],
[-28,-29,-27,-25,-22,-22,-23,-21,-24,-21,-20,-20,-22,-21,-21,-22,-22,-24,-24,-26,-20,-21,-19,-22,-23,-19,-17,-19,-17,-17,-20,-21,-21,-21,-27,-28,-24,-18,-17,-22],
[-27,-31,-30,-28,-24,-23,-20,-23,-21,-22,-25,-25,-27,-24,-26,-25,-22,-26,-28,-26,-23,-26,-26,-28,-30,-24,-22,-22,-23,-25,-27,-24,-26,-27,-32,-30,-24,-18,-17,-24],
[-25,-28,-23,-22,-22,-19,-21,-24,-14,-14,-19,-22,-20,-17,-18,-17,-18,-19,-18,-19,-24,-22,-18,-17,-23,-24,-25,-24,-28,-27,-27,-26,-25,-27,-23,-20,-21,-18,-15,-23],
[-19,-24,-21,-23,-23,-17,-16,-20,-17,-19,-22,-26,-29,-25,-23,-23,-22,-18,-15,-14,-16,-19,-19,-18,-23,-24,-23,-23,-22,-23,-24,-23,-23,-20,-18,-17,-18,-17,-17,-24],
[-15,-23,-21,-21,-21,-20,-20,-18,-17,-18,-19,-17,-18,-18,-19,-20,-20,-21,-20,-21,-20,-20,-22,-22,-25,-27,-27,-29,-28,-29,-27,-26,-28,-27,-26,-26,-22,-19,-18,-27],
[-15,-20,-22,-22,-22,-22,-23,-26,-27,-28,-29,-25,-28,-28,-27,-27,-30,-30,-29,-28,-29,-26,-25,-29,-31,-28,-29,-31,-30,-29,-26,-27,-26,-25,-27,-29,-27,-25,-21,-27],
[-17,-18,-19,-21,-21,-22,-22,-21,-21,-21,-20,-20,-20,-19,-20,-20,-21,-19,-18,-18,-21,-19,-20,-19,-18,-19,-20,-18,-19,-20,-22,-22,-21,-22,-20,-22,-23,-23,-21,-29]])


depth_maps_laptop = np.array([
[-0,-0,-0,-0,-1,-1,-1, 0, 1, 0, 0, 0, 0, 0, 0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0, 0, 0, 0, 0, 0,-0,-0,-0, 0, 0, 0, 1],
[-4,-4,-4,-3,-4,-4,-1,-2,-0,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,-1,-1,-1,-1,-2,-1,-1,-1,-2,-0],
[-2,-2,-2,-2,-3,-4,-2,-1,-1, 0, 0,-0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-0,-0,-1,-1,-1,-1,-1,-0],
[-2,-2,-2,-2,-2,-4,-3,-1,-1,-1,-0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-1,-1,-1,-1,-1,-1],
[-2,-2,-2,-2,-2,-3,-4,-3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-1,-1,-1,-1,-1],
[-2,-2,-2,-2,-2,-2,-3,-3,-3,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-1,-1,-1,-0],
[-2,-2,-2,-2,-2,-2,-2,-2,-3,-0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-1,-1,-1,-1,-1,-2,-1,-1,-1,-0,-0,-0,-1,-1,-0],
[-2,-2,-2,-2,-2,-2,-2,-2,-3, 0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-3,-2,-2,-3,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-1,-1,-0],
[-2,-2,-2,-2,-2,-2,-2,-2,-3,-0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-1,-1,-0],
[-2,-3,-2,-2,-2,-2,-2,-2,-3, 0, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-0,-1,-0],
[-2,-2,-2,-2,-2,-2,-3,-3,-3, 0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-0,-0,-1,-0],
[-1,-1,-2,-1,-1,-2,-2,-3,-3, 0,-0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-1,-1,-1,-2,-2,-2,-1,-1,-1,-1,-1,-0,-0,-0,-0,-0,-0,-1,-0],
[-1,-2,-2,-1,-0,-1,-2,-3,-3,-2,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-1,-1,-1,-2,-2,-2,-2,-1,-1,-1,-1,-0,-0,-0,-0,-0,-0,-1,-0],
[-1,-2,-2,-2,-2,-3,-3,-2,-3,-1,-1,-1,-0,-1,-1,-1,-1,-1,-1,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-0,-1,-1,-1,-0],
[-1,-1,-3,-3,-2,-2,-3,-3,-3,-3,-2,-1,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-0,-0,-0,-0,-0,-0,-0,-1,-2,-2,-1,-1],
[-1,-2,-2,-2,-3,-2,-2,-1,-1,-2,-1,-1,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-0,-0,-0,-0,-1,-2,-2,-3,-1],
[ 0,-1,-0,-1,-1,-1,-2,-2,-1,-1,-0,-0,-0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-3,-3,-4,-3,-2,-1,-0,-0,-1,-1,-2,-2, 0],
[ 0,-1,-0,-1,-1,-1,-1,-1,-0,-1,-0,-0,-0,-1,-1,-1,-1,-1,-1,-1,-2,-2,-1,-1,-0,-1,-2,-3,-1,-3,-4,-3,-1,-0,-1,-1,-1,-2,-2, 0],
[-0,-1,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-1,-1,-1,-1,-1,-1,-1,-2,-1,-1,-2,-1,-1,-1,-3,-5,-3,-3,-3,-1,-0,-1,-1,-1,-2,-2, 0],
[-0,-1,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-0,-1,-1,-1,-1,-1,-2,-2,-0,-1,-1,-1,-1,-0,-0,-0,-0,-0,-1,-1,-1,-1,-2,-2, 0],
[-0,-1,-1,-0,-0,-0,-0,-0,-1,-1,-1,-1,-0,-0,-0,-0,-0,-0,-1,-0,-1,-1,-2,-0, 0,-1,-0,-0,-0,-0,-0,-0,-1,-1,-1,-1,-1,-2,-2, 0],
[-0,-1,-1,-1,-0,-0,-0, 0,-0,-1, 0,-0, 0, 0, 0, 0, 0, 0,-0,-0,-1,-0,-1, 1, 1,-0,-0,-0,-0,-0,-0,-0,-0,-1,-1,-1,-2,-2,-2, 1],
[-0,-1,-1,-0,-0,-0,-1,-2,-2,-1,-2,-2,-2,-2,-2,-2,-2,-2,-1,-1,-1,-1,-2,-0, 1, 0, 0,-0,-0,-0,-0,-0,-0,-1,-0,-1,-2,-2,-2, 0],
[-0,-1,-1,-1,-3,-1,-1,-4,-5,-4,-4,-3,-3,-4,-4,-5,-5,-5,-4,-3,-4,-3,-3,-1,-2,-2,-2,-3,-3,-3,-4,-4,-4,-4,-3,-2,-3,-2,-3, 0],
[-1,-3,-2,-2,-3,-3,-4,-5,-5,-4,-5,-5,-6,-5,-6,-6,-7,-7,-5,-4,-5,-3,-4,-2,-2,-4,-4,-4,-4,-5,-5,-5,-6,-6,-4,-4,-4,-3,-2, 0],
[-2,-3,-3,-4,-4,-4,-4,-5,-5,-5,-6,-7,-7,-7,-7,-7,-7,-7,-6,-5,-4,-3,-4,-4,-5,-6,-5,-5,-5,-6,-6,-6,-6,-6,-4,-4,-3,-2,-2, 1],
[-4,-4,-4,-4,-4,-3,-3,-2,-3,-2,-3,-3,-3,-3,-3,-2,-3,-3,-2,-2,-2,-3,-3,-3,-3,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-2,-2,-2,-3, 0],
[-2,-3,-3,-3,-3,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-3,-3,-3,-2,-2,-2, 0]])

depth_maps_aideck = np.array([
[0,0,0,0,-1,-1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[-4,-4,-4,-4,-4,-4,-1,-3,0,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,-1,-1,-1,-1,-2,-1,-2,-2,-1],
[-2,-2,-3,-3,-4,-4,-1,-1,-1,-1,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,0,0,0,0,0,-1,-1,-1,-1,-1,0],
[-2,-2,-2,-2,-3,-4,-3,-2,-1,-1,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,0,0,-1,0,0,-1,-1,-1,-1,-1,-1],
[-2,-2,-2,-2,-2,-3,-4,-3,-1,-1,-1,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1,-2,-1,-1],
[-2,-2,-2,-2,-2,-2,-3,-4,-3,-2,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-1,-1,0,0,0,-1,-2,-1,-1],
[-2,-2,-2,-2,-2,-3,-3,-3,-3,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,-1,-1,-1,-2,-2,-1,-1,-1,0,0,-1,-2,-2,-1],
[-2,-3,-2,-3,-2,-2,-3,-3,-3,0,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-1,-2,-1,-1,-1,-1,-2,-2,-1,-1,-1,0,0,0,-1,-2,0],
[-2,-3,-3,-3,-3,-3,-3,-3,-3,0,-1,-1,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-2,0,-2,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,-1,-2,0],
[-2,-3,-3,-3,-3,-2,-3,-2,-3,1,0,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,-1,-2,0],
[-2,-2,-2,-2,-2,-2,-3,-3,-3,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,-1,-1,0],
[-1,-1,-2,-1,-2,-2,-3,-3,-3,1,0,-1,-1,-1,-1,-1,-1,-2,-1,-2,-2,-1,-1,-1,-2,-2,-2,-2,-1,-1,-1,-1,-1,0,0,0,0,0,-2,-1],
[-1,-2,-1,-1,-1,-1,-3,-3,-3,-2,-1,-1,-1,-1,-1,0,-1,-2,-2,-2,-2,-1,-1,-1,-1,-2,-2,-3,-1,-1,-1,-1,-1,0,0,0,0,-1,-1,0],
[-1,-2,-2,-3,-2,-2,-3,-2,-2,-1,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-1,-1,-1,-1,-2,-1,-1,-2,-1,-1,0,0,0,0,-1,-1,-1,-1,0],
[-1,-2,-3,-3,-2,-2,-3,-3,-3,-2,-2,-2,-1,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,-1,0,0,0,-1,-2,-2,-2,-1],
[-1,-2,-3,-2,-3,-2,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-2,-1,-1,0,0,0,-1,-2,-2,-3,-1],
[0,-1,-1,-2,-1,-2,-2,-2,-1,-1,-1,-1,0,-1,-1,-1,0,-1,-1,0,-1,-1,-1,-1,-1,-1,-2,-3,-3,-4,-3,-2,-1,0,-1,-1,-2,-3,-3,0],
[0,0,-1,-1,0,-1,0,-1,0,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-2,-2,-1,-1,-1,0,-1,-2,-2,-2,-3,-4,-3,-2,0,-1,-1,-1,-2,-3,0],
[0,0,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,-1,-1,-1,-2,-1,-2,-2,-1,-1,-2,-4,-5,-3,-3,-3,-1,-1,-1,-1,-2,-2,-3,0],
[0,0,-1,-1,-1,-1,0,0,0,-1,-1,-1,0,-1,-1,0,-1,0,-1,-1,-1,-2,-2,-1,-1,-1,-1,-1,0,-1,-1,0,0,-1,-1,-1,-1,-2,-3,0],
[0,0,-1,-1,-1,-1,0,0,-1,-1,-1,-1,0,0,-1,0,-1,0,-1,0,-1,-1,-2,0,0,0,-1,0,0,0,0,0,-1,-1,-1,-1,-1,-2,-3,0],
[0,-1,-1,-1,-1,-1,0,0,0,-1,0,-1,0,0,0,0,1,0,0,0,-1,-1,-1,1,1,-1,-1,0,-1,0,0,-1,0,-1,-1,-1,-1,-2,-2,1],
[0,0,-1,0,0,-1,-1,-2,-1,-1,-2,-1,-1,-2,-1,-2,-1,-2,-1,-1,-1,-1,-2,-1,1,0,0,0,0,0,0,0,-1,-1,-1,-2,-2,-2,-2,0],
[0,-1,-1,-1,-3,-2,-1,-4,-4,-4,-3,-2,-3,-4,-4,-4,-5,-5,-4,-3,-4,-3,-3,-1,-2,-2,-2,-3,-3,-3,-4,-4,-5,-4,-3,-2,-3,-3,-3,0],
[-1,-3,-1,-2,-3,-4,-4,-5,-5,-5,-6,-5,-6,-5,-5,-6,-6,-7,-5,-4,-5,-3,-4,-2,-2,-4,-4,-4,-4,-5,-5,-6,-6,-6,-5,-4,-4,-3,-3,0],
[-2,-3,-3,-5,-4,-4,-4,-5,-5,-5,-6,-6,-7,-6,-7,-7,-7,-7,-6,-5,-5,-3,-4,-4,-5,-5,-5,-5,-5,-6,-6,-6,-6,-6,-4,-4,-3,-3,-2,0],
[-4,-4,-4,-4,-4,-3,-3,-3,-3,-2,-3,-3,-3,-3,-3,-2,-3,-3,-2,-3,-2,-3,-3,-2,-3,-2,-2,-3,-2,-3,-3,-3,-3,-3,-3,-2,-2,-2,-3,1],
[-3,-3,-3,-3,-3,-2,-2,-2,-3,-3,-4,-4,-4,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-3,-3,-3,-3,-3,-3,-2,-2,-2,1]])


conf_maps_laptop = conf_maps_laptop + 40
conf_maps_aideck = conf_maps_aideck + 40
depth_maps_laptop = depth_maps_laptop + 20
depth_maps_aideck = depth_maps_aideck + 20
print(np.min(conf_maps_laptop), np.max(conf_maps_laptop)) # 2-36
print(np.min(conf_maps_aideck), np.max(conf_maps_aideck)) # 1-36

# plt.imshow(conf_maps_laptop)
# plt.imshow(conf_maps_aideck)

# plt.imshow(depth_maps_laptop)
plt.imshow(depth_maps_aideck)
plt.pause(1000)