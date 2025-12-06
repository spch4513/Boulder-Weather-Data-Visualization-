# Boulder-Weather-Data-Visualization-

[README.md](https://github.com/user-attachments/files/23973187/README.md)

~
Firefly Cosmos - Boulder Weather Data Art

What This Project Does
This project turns Boulder Colorado's 2024 weather data into a living artwork of glowing fireflies. I created 4,500 fireflies that float around the screen, and each one's appearance and behavior is controlled by real weather data from the CSV file. The fireflies move in swirling patterns and flicker like real fireflies at night.
It's basically like watching a night sky full of fireflies, but each firefly is telling you about the weather on a specific day in Boulder!

How It Looks
When you run the program, you see:

A dark blue gradient background (like a night sky)
Thousands of glowing fireflies drifting in organic swirling patterns
Different colored fireflies (blue ones = cold days, orange ones = hot days)
Different sized fireflies (small = dry days, big = rainy days)
Fireflies that pulse/flicker at different speeds

The whole thing is animated and runs at 60 frames per second so it looks really smooth.

Data Mappings (How Weather Data Controls the Art)
This was the most interesting part - figuring out how to make the data affect what you see:
1. Temperature → Color

Cold days (-25°C to 0°C): Blue fireflies
Cool days (0°C to 15°C): Cyan/teal fireflies
Warm days (15°C to 25°C): Yellow/green fireflies
Hot days (25°C to 37°C): Orange/red fireflies

I used HSL color space for this (hue, saturation, lightness) because it makes gradients easier than RGB. Claude helped me understand the HSL to RGB conversion math.
2. Precipitation → Size

Dry days (0mm rain): Small fireflies (3.5 pixels)
Wet days (up to 60mm rain): Large fireflies (12 pixels)

More rain = bigger, brighter fireflies
3. Wind Speed → Movement Speed

Calm days (low wind): Slow moving fireflies (speed limit 30)
Windy days (high wind): Fast moving fireflies (speed limit 160)

The wind data controls how fast each firefly can move through the flow field.
4. Snowfall → Flicker Rate

No snow: Slow gentle flickering (1.5 speed)
Heavy snow: Fast rapid flickering (6.0 speed)

This one was cool because snowy days make the fireflies blink faster, like they're shivering in the cold!

Project Structure (Files and Classes)
Files:

Chandrasekaran_data_art.py - Main program file

Loads the CSV data
Creates all the fireflies
Runs the animation loop
Handles pygame window and events


visual_objects.py - Class definitions

Contains all the classes and helper functions
This is where the OOP structure lives


boulder_weather.csv - Data file

366 rows (one per day in 2024)
Columns: DATE, AWND, PRCP, SNOW, TMAX, TMIN


README.md - This file you're reading!

Classes (Object-Oriented Programming):
1. Particle (Base Class)

This is the parent class for inheritance (extra credit requirement)
Has basic properties: x, y position
Has basic methods: update(), draw()
Firefly inherits from this

2. Firefly (Child Class - inherits from Particle)

Represents one firefly on screen
Attributes:

Position: x, y (inherited from Particle)
Velocity: vx, vy (how fast it's moving)
Color: RGB tuple (from temperature data)
Radius: size in pixels (from precipitation data)
speed_limit: max speed (from wind data)
flicker_rate: blink speed (from snow data)
depth: layer depth for parallax effect
trail: list of recent positions


Methods:

__init__(): constructor that sets up all the properties
apply_flow(): gets pushed by the flow field
update(): moves the firefly and updates animation (overrides parent method)
alpha(): calculates current brightness for flickering
draw(): renders the firefly with glow effect (overrides parent method)



3. FlowField (Separate Class)

Creates the swirling motion patterns
Attributes:

width, height: screen dimensions


Methods:

__init__(): sets up the field
vector(): calculates flow direction at any point



This demonstrates the inheritance requirement because Firefly inherits from Particle!
Helper Functions:

clamp(): keeps values within a range
norm(): normalizes values to 0-1 range
lerp(): linear interpolation between two numbers
hsl_to_rgb(): converts HSL color to RGB


How to Run This Program

Make sure you have Python 3 installed
Install pygame if you don't have it:

bash   pip install pygame

Put all files in the same folder:

Chandrasekaran_data_art.py
visual_objects.py
boulder_weather.csv


Run the main file:

bash   python Chandrasekaran_data_art.py

Watch the fireflies! Close the window when you're done.


Libraries Used

Python 3.x - programming language
pygame - for graphics and animation
csv module - for reading the weather data file (no pandas!)
math module - for sine, cosine, and other calculations
random module - for randomizing firefly properties
typing module - for type hints (makes code clearer)


AI Assistance Documentation
I used Claude.ai to help me understand concepts and debug issues. Here's exactly what AI helped with:
What Claude Helped Me With:
1. CSV Data Loading:
Showed me how to use csv.DictReader and handle missing data.

Code snippet I got help with:
pythondef parse_float(v: Optional[str]) -> Optional[float]:
    """Convert string to float, return None if empty or invalid"""
    if v is None or v.strip() == "":
        return None
    try:
        return float(v)
    except:
        return None
Claude explained the try-except pattern and why we need to handle None values and empty strings separately.

Code snippet I got help with:
pythonwith open(path, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        rows.append({
            "AWND": parse_float(r.get("AWND")),
            "PRCP": parse_float(r.get("PRCP")),
            # ... etc
        })
Claude showed me csv.DictReader lets me access columns by name instead of index numbers.

2. Math Library Functions:
This was tough - Claude helped me understand trigonometry for the flow field.

Code snippet I got help with:
pythondef vector(self, x: float, y: float, t: float):
    nx = x / self.width
    ny = y / self.height
    angle = (
        math.sin(nx * 3 + t * 0.2)
        + math.cos(ny * 4 - t * 0.15)
        + math.sin((nx + ny) * 2.5 + t * 0.1)
    )
    speed = 70
    return math.cos(angle) * speed, math.sin(angle) * speed
Claude explained:

math.sin() and math.cos() create wave patterns
Combining multiple sine waves at different frequencies makes complex organic motion
math.cos(angle) and math.sin(angle) convert an angle to x,y velocity components

Code snippet I got help with:
pythonspeed = math.hypot(self.vx, self.vy)
if speed > self.speed_limit:
    scale = self.speed_limit / speed
    self.vx *= scale
    self.vy *= scale
Claude explained math.hypot() calculates distance using Pythagorean theorem (sqrt(vx² + vy²)). This is how we limit speed without changing direction.
Code snippet I got help with:
pythonself.flicker_phase = random.uniform(0, math.pi * 2)
# later...
return 0.7 + 0.3 * math.sin(self.flicker_phase)
Claude explained math.pi * 2 is a full circle (360 degrees in radians), and sine waves are perfect for smooth pulsing animation.

3. Random Library:
Claude showed me how to use random for variation.

Code snippet I got help with:
pythonfor _ in range(count):
    row = random.choice(rows)  # pick random day
    x = random.uniform(0, WIDTH)  # random position
    y = random.uniform(0, HEIGHT)
    depth = random.uniform(0.4, 1.0)  # random layer
Claude explained:

random.choice(list) picks one random item from a list
random.uniform(a, b) gives a random decimal between a and b
This makes each firefly unique even though they come from same data

Code snippet I got help with:
pythonself.flicker_phase = random.uniform(0, math.pi * 2)
Starting each firefly at a random phase means they don't all blink in sync - looks more organic.

4. Color Math (HSL to RGB):
This was the HARDEST part! I didn't understand this formula at all at first.

Code snippet I got help with:
pythondef hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """Convert HSL to RGB"""
    c = (1 - abs(2 * l - 1)) * s
    hp = (h / 60) % 6
    x = c * (1 - abs(hp % 2 - 1))
    r = g = b = 0
    if 0 <= hp < 1:
        r, g, b = c, x, 0
    elif 1 <= hp < 2:
        r, g, b = x, c, 0
    # ... etc for all 6 color segments
    m = l - c / 2
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
Claude broke down every line:

c is chroma (color intensity)
hp figures out which segment of color wheel (0-6)
The if/elif chain sets RGB based on which segment
m adjusts for lightness
Multiply by 255 to convert 0-1 range to 0-255 for pygame

Code snippet I got help with:
pythont_norm = norm(tavg, stats["TMIN_min"], stats["TMAX_max"])
hue = lerp(210, 35, t_norm)  # blue to orange
sat = lerp(0.45, 0.75, t_norm)
light = 0.60
color = hsl_to_rgb(hue, sat, light)
Claude explained using HSL makes smooth color gradients WAY easier than trying to interpolate RGB directly.

5. Normalization and Linear Interpolation:

Claude helped me understand these fundamental mapping functions.

Code snippet I got help with:
pythondef norm(value: Optional[float], vmin: float, vmax: float) -> float:
    """Normalize value to 0-1 range"""
    if value is None:
        return 0.0
    if vmax == vmin:
        return 0.0
    t = (value - vmin) / (vmax - vmin)
    return clamp(t, 0.0, 1.0)
Claude explained this converts any range (like -25°C to 37°C) into 0-1, making it easy to map to other ranges.

Code snippet I got help with:
pythondef lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b"""
    return a + (b - a) * clamp(t, 0.0, 1.0)
Claude explained lerp is the opposite of norm - it takes a 0-1 value and converts it to any range you want.

Using them together:
pythonp_norm = norm(row["PRCP"], stats["PRCP_min"], stats["PRCP_max"])
radius = lerp(3.5, 12, p_norm)
This maps precipitation (any range) → 0-1 → size (3.5-12 pixels). Claude showed me this is the standard way to map data to visuals.

6. Pygame Transparency and Glow Effects:
Claude helped me figure out why my circles looked wrong at first.

Code snippet I got help with:
pythondef draw(self, surface):
    import pygame
    a = clamp(self.alpha(), 0, 1)
    for i in range(3, 0, -1):
        r = int(self.radius * (i / 3))
        strength = int(a * (80 + 40 * i))
        glow = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*self.color, strength), (r + 1, r + 1), r)
        surface.blit(glow, (int(self.x) - r, int(self.y) - r))

Claude explained:

pygame.SRCALPHA flag lets surfaces have transparent pixels
Need to create temp surface for each layer
Draw multiple circles with decreasing alpha creates glow
(*self.color, strength) unpacks RGB tuple and adds alpha value


7. Inheritance Implementation:
Claude suggested adding this for extra credit.

Code snippet I got help with:
pythonclass Particle:
    """Base class for visual particles"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self, dt):
        pass
    
    def draw(self, surface):
        pass

class Firefly(Particle):  # Inherits from Particle
    def __init__(self, x, y, color, radius, speed_limit, flicker_rate, depth):
        super().__init__(x, y)  # Call parent constructor
        # ... rest of firefly properties
Claude explained:

Parent class defines common properties
super().__init__(x, y) calls parent's constructor to set x, y
Child class adds more specific properties
This avoids repeating x, y initialization code


8. Screen Wrapping Logic:
Claude helped me understand the modulo approach.

Code snippet I got help with:
python# wrap around screen edges
if self.x < 0: self.x += w
if self.x > w: self.x -= w
if self.y < 0: self.y += h
if self.y > h: self.y -= h
This makes fireflies wrap like Pac-Man - when they go off one edge, they appear on the opposite edge.

9. Computing Statistics for Normalization:

Claude showed me this pattern.
Code snippet I got help with:
pythondef compute_stats(rows: List[Dict]) -> Dict[str, float]:
    stats = {}
    keys = ["AWND", "PRCP", "SNOW", "TMAX", "TMIN"]
    for k in keys:
        vals = [r[k] for r in rows if r[k] is not None]
        stats[f"{k}_min"] = min(vals) if vals else 0
        stats[f"{k}_max"] = max(vals) if vals else 1
    return stats
Claude explained we need min/max of each column to normalize properly. The list comprehension filters out None values before finding min/max.

What I Wrote Myself:

All the actual code implementation
The creative decisions (how to map data to visuals)
The specific numbers and parameters (like flicker rates, colors, sizes)
How many fireflies to create
The gradient background function
The overall design and aesthetic choices
