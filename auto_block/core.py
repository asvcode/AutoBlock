# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['autoblock']

# Cell
import os

from fastai.basics import *
from fastai.callback.all import *
from fastai.vision.all import *

# Cell
def autoblock(dir, y_col=None, train_folder='train', csv='train', seg=False, seg_fold='masks'):
    """Automatically create a datablock"""
    files = os.listdir(dir)
    print(f'>> Files & Folders: {files}\n')
    if seg == False:
        print('>> Non segmentation')
        try:
            for f in files:
                if f.endswith('.csv'):
                    autoblock.read_csv = pd.read_csv(f'{dir}/{csv}.csv')
                    print(autoblock.read_csv.head(1))
                    for fil in os.listdir(f'{dir}/{train_folder}'):
                        if fil.endswith('.jpg'):
                            autoblock.get_x = lambda x:f'{dir}/{train_folder}/{x[0]}.jpg'
                            autoblock.block_cls = PILImage
                            break
                        elif fil.endswith('dcm'):
                            autoblock.get_x = lambda x:f'{dir}{train_folder}/{x[0]}.dcm'
                            autoblock.block_cls = PILDicom
                            break
                        else:
                            print('unable to process')
                            break

                    bl = DataBlock(blocks=(ImageBlock(cls=autoblock.block_cls), CategoryBlock),
                            get_x = autoblock.get_x,
                            get_y = Pipeline(ColReader(y_col)),
                            item_tfms=Resize(224),
                            batch_tfms=[Normalize.from_stats(*imagenet_stats)]
                            )
                    dls = bl.dataloaders(autoblock.read_csv, bs=16)
                    print('>> working....')
                    dls.show_batch()
                    break

                else:
                    print('>> No csv file detected')
                    fil = get_files(f'{dir}/{train_folder}', recurse=True)
                    fileone = fil[0]
                    print(fileone)
                    filename, file_extension = os.path.splitext(fileone)
                    if file_extension == '.JPEG':
                        autoblock.cls_select=PILImage
                        autoblock.get_items = get_image_files
                    elif file_extension == '.png':
                        autoblock.cls_select=PILImage
                        autoblock.get_items = get_image_files
                    elif file_extension == '.jpg':
                        autoblock.cls_select=PILImage
                        autoblock.get_items = get_image_files
                    elif file_extension == '.dcm':
                        autoblock.cls_select=PILDicom
                        autoblock.get_items = get_dicom_files
                    else:
                        print('format not found')
                    bl = DataBlock(blocks=(ImageBlock(cls=autoblock.cls_select), CategoryBlock),
                            get_items = autoblock.get_items,
                            get_y = parent_label,
                            item_tfms=Resize(224),
                            batch_tfms=[Normalize.from_stats(*imagenet_stats)]
                                )
                    dls = bl.dataloaders(f'{dir}', bs=16)
                    print('>> working....')
                    dls.show_batch()
                    break
        except FileNotFoundError:
            print('>> specify correct csv file from those listed')
        except AttributeError:
            print(">> specify correct 'column' from csv tags in y_col field")
        except IndexError:
            print(">> Check 'train' folder")
        except TypeError:
            print('Please check source - NoneType returned')

    if seg == True:
        print('>> Segmentation')
        get_msk = lambda o: f'{dir}/{seg_folder}/{o.stem}{o.suffix}'
        try:
            fil = get_files(f'{dir}/{train_folder}', recurse=True)
            fileone = fil[0]
            print(fileone)
            filename, file_extension = os.path.splitext(fileone)
            if file_extension == '.JPEG':
                cls_select=PILImage
            elif file_extension == '.png':
                cls_select=PILImage
            elif file_extension == '.jpg':
                cls_select=PILImage
            elif file_extension == '.PNG':
                cls_select=PILImage
            elif file_extension == '.dcm':
                cls_select=PILDicom
            else:
                print('format not found')
            bl = DataBlock(blocks=(ImageBlock(cls=PILImage), MaskBlock),
                        get_items = get_image_files,
                        get_y = get_msk,
                        item_tfms=Resize(224),
                        batch_tfms=[Normalize.from_stats(*imagenet_stats)]
                            )
            dls = bl.dataloaders(f'{dir}{train_folder}', bs=16)
            print('>> working....')
            dls.show_batch()
        except FileNotFoundError:
            print('csv file not found')
        except AttributeError:
            print('column not found')
        except IndexError:
            print(">> Check 'train' folder")
        except TypeError:
            print('auto_block needs to have source and y_col(even if there is no csv file)')