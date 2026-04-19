#complete your tasks in this file
#Task 1: Defining DataClasses 
import math
from dataclasses import dataclass 
@dataclass (frozen= True) 
class GlobeRect: 
    lo_lat: float 
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen= True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str  #ocean, mountain, forest, other 

@dataclass(frozen= True)
class RegionCondition: 
    region: Region 
    year: int
    pop: int 
    ghg_rate: float

#Task 2: Create Sample Data 

#1. Major Metropolitain Area - New York 
NY_rect = GlobeRect(40.5, 41, -74.3, -73.7)
NY_region= Region(NY_rect, "New York", "other") 
NY_condition = RegionCondition(NY_region, 2025,20000000, 50000000)

#2. Major Metropolitain Outside Country- Tokyo 
Tokyo_rect = GlobeRect(35.5,36, 139.5, 140)
Tokyo_region = Region (Tokyo_rect, "Tokyo", "other")
Tokyo_condition = RegionCondition(Tokyo_region,2025, 14000000, 40000000)

#3. Ocean Region - part of Pacific Ocena 
Pacific_rect = GlobeRect(10, 20, -150, -130)
Pacific_region= Region(Pacific_rect, "Central Pacific", "ocean")
Pacific_condition = RegionCondition(Pacific_region, 2025,0, 1000000)

#4. Region around SLO 
SLO_rect = GlobeRect(35,35.5, -120.8, -120.3) 
SLO_region = Region(SLO_rect, "San Luis Obispo Area","other")
SLO_condition = RegionCondition(SLO_region, 2025, 500000,2000000.0 )

#Final List 
region_conditions = [NY_condition, Tokyo_condition, Pacific_condition, SLO_condition]

#Task 3 Implement External Functions (with Design Receipe)

#3.1 Emissions per Capita     
def emissions_per_capita(rc: RegionCondition)-> float: 
    ##Return Greenhouse gas emissions per person / per year ##
    if rc.pop == 0: 
        return 0.0
    return (rc.ghg_rate / rc.pop)

#3.2 Area(gr)
                                    # A = R^2 * |λ₂ - λ₁| * |sin(φ₂) - sin(φ₁)|
                                    # R = 6378.1 (Earth’s radius in kilometers)
                                    # λ₁, λ₂ = west and east longitude (in radians)
                                    # φ₁, φ₂ = low and high latitude (in radians)

def area(gr:GlobeRect) -> float:  #surface are of the globerect using spherical Earth 
    r = 6378.1  #earth radius 
#convert degrees to radians 
    lo_lat_rad= math.radians(gr.lo_lat)
    hi_lat_rad = math.radians(gr.hi_lat) 
    west_long_rad = math.radians(gr.west_long)     
    east_long_rad = math.radians(gr.east_long)
#find longitude 
    long_diff = east_long_rad -  west_long_rad
    if long_diff<0:
     long_diff = long_diff + (2*math.pi)
#finding area - Formula: A = R^2 * |Δλ| * |sin(φ2) - sin(φ1)|
    return ((r**2)* abs(long_diff) * abs(math.sin(hi_lat_rad)- math.sin(lo_lat_rad)))

#3.3 Emissions per Square KM 
def emissions_per_square_km(rc:RegionCondition)-> float: 
    region_area = area(rc.region.rect)
#Return ghg emissions per sq km 
    if region_area == 0: 
        return 0.0
    return rc.ghg_rate/region_area


#3.4 Densest (rc_list)- recursive 
def population_density(rc: RegionCondition)-> float: # helper to find density: pop/area
    region_area = area(rc.region.rect)
    if region_area == 0: 
        return 0.0
    return rc.pop / region_area

def find_densest(rc_list: list[RegionCondition]): 
#helps rerurign the actual Region Condition object with the highest density 
    if len(rc_list) ==1: 
        return rc_list[0]
    
    densest_rest= find_densest(rc_list[1:])

    if population_density(rc_list[0]) >= population_density(densest_rest): 
        return rc_list[0] #fitst element 
    return densest_rest 
    
def densest(rc_list: list[RegionCondition])-> str: #main func (gives name of region)
   return (find_densest(rc_list)).region.name


# Task 4: Simulate Future Projections 

#4.1 project conditions (rc, years)
def growth_rate(terrain: str) -> float:
#Return the annual population growth rate for a terrain type.
    rates= {"ocean": 0.0001, "mountains":0.0005, "forest":-0.00001}
    return rates.get(terrain, 0.0003)

def project_population(pop: int, rate: float, years: int) -> int:
#projected population after a number of years. Applies the growth rate once per year.
    if years == 0:
        return pop
    return int(project_population(pop, rate, years - 1) * (1 + rate))

def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
#Return a new RegionCondition projected forward by the years that have passed.
    rate = growth_rate(rc.region.terrain)
    new_pop = project_population(rc.pop, rate, years)

    if rc.pop == 0:
        new_ghg_rate = 0.0
    else:
        new_ghg_rate = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(rc.region,rc.year + years, new_pop,new_ghg_rate)


