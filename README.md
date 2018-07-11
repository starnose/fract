# fract
Fractal Drawer in python, focusing on drawing many different 2d fractal types

This program can currently draw, at arbitrary resolution and zoom -

* Mandelbrot sets (any power, inverse)
* Julia sets (any power, inverse, and glynn-trees)
* Polar-inverse Mandelbrot sets (Mandel-drop)
* Burning ship fractals
* Newton fractals 
* Mandelbar sets
* Pickover Biomorphs

These can be output as greyscale or colour. For colour, various colouring strategies are available. 

Most of the simpler fractal types use a smooth/log shading algorithm as described here - https://linas.org/art-gallery/escape/smooth.html
Newton fractals use raw z-value output, though when the log shading is applied they grow extra features which are interesting, even if I don't fully understand them at present.

This is coupled with a colour-range system that interpolates between arbitrary colour sequences and can scale colour output (currently fractional exponent scaling is good).

Future work:
* Phoenix fractals
* Log colour scaling
* Orbital-Trap style colouring

Far future work:
* Ray marching and mandelbulbs. Maybe.
