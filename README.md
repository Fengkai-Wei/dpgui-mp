# **DearPyGui for MEEP**
## Platform
* Linux
* macOS
  
This GUI is for MEEP package who doesn't support Windows. WSL is a compromised option for Windows users (like me).

Please check the [installation page of MEEP](https://meep.readthedocs.io/en/latest/Installation/#installation) for more info.


## Depedencies

## Key Modifications for Visualisation
MEEP dosen't have its native GUI, therefore some modifications must be applied to resolve problems in GUI and visualisation. Most of them involve the meep source code and I prefer to report them in MEEP repo rather than publish my own narrowed version of MEEP. Here I only list key changes in meep code:

### 1.Memory/Thread Conflicts
In `meep.Simulation.Plot3D()`, a `SceneCanvas` object is created but never be deleted after calling this function. It is better to add:
~~~
def Plot3d(....)
    ....
    canvas.show(run=True)
    
    # This line kills the memory used by canvas
    canvas.close()
~~~

Otherwise the whole program will be (frequently) termitated by Errors like SegFault or corrupted double-linked list.

### 2. 3D colour map
Unlike `Plot2D`, the function of `Plot3D()` has no kwarg of frequency, which means the colour of material purely depends on its $\varepsilon_r$ at 0.0 frequency by `get_eps_grid()` in `Plot3D`:
~~~
    eps_data = np.round(np.real(sim.get_epsilon_grid(xtics, ytics, ztics), 2))
~~~
And the definition is:
~~~
def get_epsilon_grid(
    self,
    xtics: np.ndarray = None,
    ytics: np.ndarray = None,
    ztics: np.ndarray = None,
    frequency: float = 0.0,
):
~~~
Many materials have $\varepsilon_r$ = 1.0, which they show no difference of colour between air(or vaccum, the background material) and themselves.

Here I add a c-Si cylinder and specify freq = 1/1.55, please check the difference after correctly passing frequency:
|  Old   | New  |
|  ----  | ----  |
| ![image](https://github.com/user-attachments/assets/6aea3992-fee7-4366-b714-ae03cb9d4648)| ![image](https://github.com/user-attachments/assets/15f6fdbd-72dc-48d6-a210-833d9e48abe2)
 |
