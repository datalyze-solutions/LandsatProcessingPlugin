from copy import deepcopy

MD_product_metadata = 'PRODUCT_METADATA'
MD_image_attributes = 'IMAGE_ATTRIBUTES'
MD_sun_elevation = 'SUN_ELEVATION'
MD_file_name_band_1 = 'FILE_NAME_BAND_1'
MD_file_name_band_2 = 'FILE_NAME_BAND_2'
MD_file_name_band_3 = 'FILE_NAME_BAND_3'
MD_file_name_band_4 = 'FILE_NAME_BAND_4'
MD_file_name_band_5 = 'FILE_NAME_BAND_5'
MD_file_name_band_6 = 'FILE_NAME_BAND_6'
MD_file_name_band_6v1 = 'FILE_NAME_BAND_6_VCID_1'
MD_file_name_band_6v2 = 'FILE_NAME_BAND_6_VCID_2'
MD_file_name_band_7 = 'FILE_NAME_BAND_7'
MD_file_name_band_8 = 'FILE_NAME_BAND_8'
MD_spacecraft_id = 'SPACECRAFT_ID'
MD_date_acquired = 'DATE_ACQUIRED'
MD_scene_center_time = 'SCENE_CENTER_TIME'
MD_reflective_lines = 'REFLECTIVE_LINES'
MD_reflective_samples = 'REFLECTIVE_SAMPLES'
MD_thermal_lines = 'THERMAL_LINES'
MD_thermal_samples = 'THERMAL_SAMPLES'

solar_elevation_min = 0.
solar_elevation_max = 90.
landsat_type_5 = 'LANDSAT_5'
landsat_type_7 = 'LANDSAT_7'
landsat_types = [landsat_type_5, landsat_type_7]

# metadata dummies
landsatMetadataDummy = {
          MD_image_attributes: {
              MD_sun_elevation: None
          },
          MD_product_metadata: {
              MD_thermal_lines: None,
              MD_thermal_samples: None,
              MD_reflective_samples: None,
              MD_reflective_lines: None,
              MD_scene_center_time: None,
              MD_date_acquired: None,
              MD_file_name_band_1: None,
              MD_file_name_band_2: None,
              MD_file_name_band_3: None,
              MD_file_name_band_4: None,
              MD_file_name_band_5: None,
              MD_file_name_band_7: None,
              MD_spacecraft_id: None
          }
      }
landsat5MetadataDummy = deepcopy(landsatMetadataDummy)
landsat5MetadataDummy[MD_product_metadata][MD_file_name_band_6] = None

landsat7MetadataDummy = deepcopy(landsatMetadataDummy)
landsat7MetadataDummy[MD_product_metadata][MD_file_name_band_6v1] = None
landsat7MetadataDummy[MD_product_metadata][MD_file_name_band_6v2] = None
landsat7MetadataDummy[MD_product_metadata][MD_file_name_band_8] = None