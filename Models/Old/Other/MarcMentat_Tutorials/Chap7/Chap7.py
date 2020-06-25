#   Imports

from py_mentat import *
from py_post import *

def main():

    py_send("*new_model yes *open_model sets.mfd")

    m = py_get_int("nsets()")
    print("Found ", m, " sets")

    for i in range(1, m + 1):

        id = py_get_int("set_id(%d)" % i)
        sn = py_get_string("set_name(%d)" % id)
        st = py_get_string("set_type(%d)" % id)
        n = py_get_int("nset_entries(%d)" % id)

        if stype not in ("icond", "apply", "lcase"):

            print("Set ", sn, " is a ", stype, " set with ", n, " entries")

            for j in range(1, n + 1):

                k = py_get_int("set_entry(%d,%d)" % (id, j))
                print("   entry ", j, " is ", k)

                if (stype == 'face'):

                    l = py_get_int("set_edge(%d,%d)" % (id, j))
                    print("   face number ", l)

                elif (stype == 'edge'):
                    
                    l = py_get_int("set_edge(%d,%d)" % (id, j))
                    print("   edge number ", l)

                else:

                    print("   ")
    
    print("   ")

    m = py_get_int("ncbodys()")
    print("Found ", m, " contact bodies")

    for i in range(1, m + 1):
        
        sn = py_get_string("cbody_name_index(%d)" % i)
        id = py_get_int("cbody_id(%s)" % sn)

        print("contact body ", i, " id ", id, " name ", sn)

    m = py_get_int("nmaters()")
    print("\nMaterials ", m)

    for i in range(1, m + 1):

        sn = py_get_string("mater_name_index(%d)" % i)
    

    sn = py_get_string("mater_name()")
    print("   current material: ", sn)

    st = py_get_string("mater_type(%s)" % sn)
    print("   type: ", st)

    e = py_get_data("mater:structural:youngs_modulus")
    print("   Young's modulus: ", e)

    p = py_get_data("mater:structural:poissons_ratio()")
    print("   Poisson's ratio: ", p)

    ys = py_get_data("mater:structural:yield_stress")
    print("   yield stress: ", ys)

    print("   ")

    sn = py_get_string("ctable_name()")
    print("   contact table   ", sn)

    sn = "contact_table:the_mesh:refined_mesh:dist_tol"
    dt = py_get_data(sn)
    print("   contact distance tolerance: ", dt)

    print("   ")

    sn = py_get_string("geom_name()")
    print("   current geometry data: ", sn)

    thick = py_get_data("geometry:thick")
    print("   thickness: ", thick)

    print("   ")

    

