import cv2
import gc
import numpy as np
import rasterio



def pansharpen(m, pan, psh, R = 1, G = 2, B = 3, NIR = 4, method = 'simple_brovey', W = 0.1):
    """ 
    This function is used to pansharpen a given multispectral image using its corresponding panchromatic image via one of 
    the following algorithms: 'simple_brovey, simple_mean, esri, brovey'.
  
    Inputs:
    - m: File path of multispectral image to undergo pansharpening
    - pan: File path of panchromatic image to be used for pansharpening
    - psh: File path of pansharpened multispectral image to be written to file
    - R: Band number of red band in the multispectral image
    - G: Band number of green band in the multispectral image
    - B: Band number of blue band in the multispectral image
    - NIR: Band number of near - infrared band in the multispectral image
    - method: Method to be used for pansharpening
    - W: Weight value to be used for brovey pansharpening methods
  
    Outputs:
    - img_psh: Pansharpened multispectral image
  
    """
  
    with rasterio.open(m) as f:
        metadata_ms = f.profile
        img_ms = np.transpose(f.read(tuple(np.arange(metadata_ms['count']) + 1)), [1, 2, 0])
    
    with rasterio.open(pan) as g:
        metadata_pan = g.profile
        img_pan = g.read(1)
    

  
    ms_to_pan_ratio = metadata_ms['transform'][0] / metadata_pan['transform'][0]
    rescaled_ms = cv2.resize(img_ms, dsize = None, fx = ms_to_pan_ratio, fy = ms_to_pan_ratio, 
                             interpolation = cv2.INTER_CUBIC).astype(metadata_ms['dtype'])

  
    if img_pan.shape[0] < rescaled_ms.shape[0]:
        ms_row_bigger = True
        rescaled_ms = rescaled_ms[: img_pan.shape[0], :, :]
    else:
        ms_row_bigger = False
        img_pan = img_pan[: rescaled_ms.shape[0], :]
        
    if img_pan.shape[1] < rescaled_ms.shape[1]:
        ms_column_bigger = True
        rescaled_ms = rescaled_ms[:, : img_pan.shape[1], :]
    else:
        ms_column_bigger = False
        img_pan = img_pan[:, : rescaled_ms.shape[1]]
  
    del img_ms; gc.collect()
  
  
    if ms_row_bigger == True and ms_column_bigger == True:
        img_psh = np.zeros((img_pan.shape[0], img_pan.shape[1], rescaled_ms.shape[2]), dtype = metadata_pan['dtype'])
    elif ms_row_bigger == False and ms_column_bigger == True:
        img_psh = np.zeros((rescaled_ms.shape[0], img_pan.shape[1], rescaled_ms.shape[2]), dtype = metadata_pan['dtype'])
        metadata_pan['height'] = rescaled_ms.shape[0]
    elif ms_row_bigger == True and ms_column_bigger == False:
        img_psh = np.zeros((img_pan.shape[0], rescaled_ms.shape[1], rescaled_ms.shape[2]), dtype = metadata_pan['dtype'])
        metadata_pan['width'] = rescaled_ms.shape[1]
    else:
        img_psh = np.zeros((rescaled_ms.shape), dtype = metadata_pan['dtype'])
        metadata_pan['height'] = rescaled_ms.shape[0]
        metadata_pan['width'] = rescaled_ms.shape[1]
    

    
    if method == 'simple_brovey':
        all_in = rescaled_ms[:, :, R - 1] + rescaled_ms[:, :, G - 1] + rescaled_ms[:, :, B - 1] + rescaled_ms[:, :, NIR - 1]
        for band in range(rescaled_ms.shape[2]):
            img_psh[:, :, band] = np.multiply(rescaled_ms[:, :, band], (img_pan / all_in))
        
  
    if method == 'simple_mean':
        for band in range(rescaled_ms.shape[2]):
            img_psh[:, :, band] = 0.5 * (rescaled_ms[:, :, band] + img_pan)
    
        
    if method == 'esri':
        ADJ = img_pan - rescaled_ms.mean(axis = 2)
        for band in range(rescaled_ms.shape[2]):
            img_psh[:, :, band] = rescaled_ms[:, :, band] + ADJ
        
    
    if method == 'brovey':
        DNF = (img_pan - W * rescaled_ms[:, :, NIR - 1]) / (W * rescaled_ms[:, :, R - 1] + W * rescaled_ms[:, :, G - 1] + W * rescaled_ms[:, :, B - 1])
        for band in range(rescaled_ms.shape[2]):
            img_psh[:, :, band] = rescaled_ms[:, :, band] * DNF
        
  
    del img_pan, rescaled_ms; gc.collect()
  
    
    metadata_pan['count'] = img_psh.shape[2]
    with rasterio.open(psh, 'w', **metadata_pan) as dst:
        dst.write(np.transpose(img_psh, [2, 0, 1]))
  
    return img_psh
