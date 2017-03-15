def my_interpolate_3D2D_altitude(cube_in,cube_grid,coordinates_in=None,coordinates_out=None,method='linear'):
   import numpy as np
   from scipy.interpolate import RegularGridInterpolator,interp1d

   #Calculate input grid for griddate method
   print(cube_in.summary(True))
   print(coordinates_in)

   source_points=[cube_in.coord(c).points for c in coordinates_in]
   source_points_interp=tuple(source_points)

   #Calculate output grid for griddate method
   mesh_coord_0,mesh_coord_1=np.meshgrid(cube_in.coord(coordinates_in[0]).points,cube_grid.coord(coordinates_in[1]).points,indexing='ij')
   mesh_coord_0,mesh_coord_2=np.meshgrid(cube_in.coord(coordinates_in[0]).points,cube_grid.coord(coordinates_in[2]).points,indexing='ij')
   target_points_interp=np.stack(tuple([mesh_coord_0.flatten(),mesh_coord_1.flatten(),mesh_coord_2.flatten()])).T
   #Calcululate interpolate output and bring it into the right shape:
       
   Interpolator=RegularGridInterpolator(source_points_interp,cube_in.data,method=method,bounds_error=False,fill_value=0)

   target_data=Interpolator(target_points_interp).reshape((cube_in.data.shape[0],cube_grid.coord(coordinates_out[1]).shape[0]))

   Interpolator_altitude=RegularGridInterpolator(source_points_interp,cube_in.coord(coordinates_out[0]).points,method=method,bounds_error=False,fill_value=0)
   altitude_data=Interpolator_altitude(target_points_interp).reshape((cube_in.data.shape[0],cube_grid.coord(coordinates_out[1]).shape[0]))

   target_data_altitude=np.nan*np.ones(cube_grid.data.shape)
   for i in range(target_data_altitude.shape[-1]):
       target_data_altitude_interpolator=interp1d(altitude_data[:,i],target_data[:,i],bounds_error=False,fill_value=0)
       target_data_altitude[...,i]=target_data_altitude_interpolator(cube_grid.coord(coordinates_out[0]).points)
   
   #Store output in cube and adjust metadata:
   cube_out=cube_grid.copy()
   cube_out.data=target_data_altitude
   cube_out.rename(cube_in.name())
   cube_out.units=cube_in.units

   return(cube_out)




def my_interpolate_3D2D(cube_in,cube_grid,coordinates,method='linear'):
   import numpy as np
   from scipy.interpolate import RegularGridInterpolator
   
   
   #Calculate input grid for griddate method
   source_points=[cube_in.coord(c).points for c in coordinates]
   source_points_interp=tuple(source_points)

   #Calculate output grid for griddate method
   mesh_coord_0,mesh_coord_1=np.meshgrid(cube_grid.coord(coordinates[0]).points,cube_grid.coord(coordinates[1]).points,indexing='ij')
   mesh_coord_0,mesh_coord_2=np.meshgrid(cube_grid.coord(coordinates[0]).points,cube_grid.coord(coordinates[2]).points,indexing='ij')
   target_points_interp=np.stack(tuple([mesh_coord_0.flatten(),mesh_coord_1.flatten(),mesh_coord_2.flatten()])).T
   
   #Calcululate interpolate output and bring it into the right shape:
       
   Interpolator=RegularGridInterpolator(source_points_interp,cube_in.data,method=method,bounds_error=False,fill_value=0)
   print(Interpolator(target_points_interp).shape)
   print(cube_grid.data.shape)
   target_data=Interpolator(target_points_interp).reshape(cube_grid.data.shape)
   
   #Store output in cube and adjust metadata:
   cube_out=cube_grid.copy()
   cube_out.data=target_data
   cube_out.rename(cube_in.name())
   cube_out.units=cube_in.units


   return(cube_out)


#def my_interpolate_3D2D_altitude(cube_in,cube_grid,coordinates,method='linear'):
#   import numpy as np
#   from scipy.interpolate import griddata
#
#   #Calculate input grid for griddate method
#   mesh_coord_0,mesh_coord_1,mesh_coord_2=np.meshgrid(cube_in.coord(dimensions=0).points,cube_in.coord(coordinates[1]).points,cube_in.coord(coordinates[2]).points,indexing='ij')
#   coord_0=cube_in.coord(coordinates[0]).points
#   source_points_interp=np.stack(tuple([coord_0.flatten(),mesh_coord_1.flatten(),mesh_coord_2.flatten()])).T
#     
#   #Calculate output grid for griddate method
#   mesh_coord_0,mesh_coord_1=np.meshgrid(cube_grid.coord(coordinates[0]).points,cube_grid.coord(coordinates[1]).points,indexing='ij')
#   mesh_coord_0,mesh_coord_2=np.meshgrid(cube_grid.coord(coordinates[0]).points,cube_grid.coord(coordinates[2]).points,indexing='ij')
#   target_points_interp=np.stack(tuple([mesh_coord_0.flatten(),mesh_coord_1.flatten(),mesh_coord_2.flatten()])).T
#   
#   #Put data input into the right shape:
#   data_array=cube_in.data.flatten()
#   
#   #Calcululate interpolate output and bring it into the right shape:
#   target_data=griddata(source_points_interp,data_array,target_points_interp).reshape(cube_grid.data.shape)
#
#   #Store output in cube and adjust metadata:
#   cube_out=cube_grid.copy()
#   cube_out.data=target_data
#   cube_out.rename(cube_in.name())
#   cube_out.units=cube_in.units
#
#   return(cube_out)