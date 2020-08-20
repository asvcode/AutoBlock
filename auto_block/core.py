# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['auto_block']

# Cell
import os

from fastai2.basics import *
from fastai2.callback.all import *
from fastai2.vision.all import *

# Cell
def auto_block(dir, y_col, train_fol='train', csv='train', seg=False, seg_fold='masks'):
    files = os.listdir(dir)
    print(files)
    if seg == False:
        print('Non segmentation')
        try:
            for f in files:
                if f.endswith('.csv'):
                    print('csv found')
                    auto_block.read_csv = pd.read_csv(f'{dir}/{csv}.csv')
                    print(auto_block.read_csv.head(1))
                    for fil in os.listdir(f'{dir}/{train_fol}'):
                        if fil.endswith('.jpg'):
                            auto_block.get_x = lambda x:f'{dir}/{train_fol}/{x[0]}.jpg'
                            auto_block.block_cls = PILImage
                            break
                        elif fil.endswith('dcm'):
                            auto_block.get_x = lambda x:f'{dir}{train_fol}/{x[0]}.dcm'
                            auto_block.block_cls = PILDicom
                            break
                        else:
                            print('unable to process')
                            break

                    bl = DataBlock(blocks=(ImageBlock(cls=auto_block.block_cls), CategoryBlock),
                            get_x = auto_block.get_x,
                            get_y = Pipeline(ColReader(y_col)),
                            item_tfms=Resize(224),
                            batch_tfms=[Normalize.from_stats(*imagenet_stats)]
                            )
                    dls = bl.dataloaders(auto_block.read_csv, bs=16)
                    dls.show_batch()
                    break

                else:
                    print('default train.csv does not exist')
                    fil = get_files(f'{dir}/{train_fol}', recurse=True)
                    fileone = fil[0]
                    print(fileone)
                    filename, file_extension = os.path.splitext(fileone)
                    print(filename, file_extension)
                    if file_extension == '.JPEG':
                        cls_select=PILImage
                        print('JPEG')
                    if file_extension == '.png':
                        cls_select=PILImage
                        print('png')
                    if file_extension == '.jpg':
                        cls_select=PILImage
                        print('jpg')
                    if file_extension == '.dcm':
                        cls_select=PILDicom
                        print('dcm')
                    else:
                        print('format not found')
                    bl = DataBlock(blocks=(ImageBlock(cls=PILImage), CategoryBlock),
                            get_items = get_image_files,
                            get_y = parent_label,
                            item_tfms=Resize(224),
                            batch_tfms=[Normalize.from_stats(*imagenet_stats)]
                                )
                    dls = bl.dataloaders(dir, bs=16)
                    dls.show_batch()
                    break
    if seg == True:
        print('At Segmentation')
        get_msk = lambda o: f'{dir}/{seg_fold}/{o.stem}{o.suffix}'
        try:
            fil = get_files(f'{dir}/{train_fol}', recurse=True)
            fileone = fil[0]
            print(fileone)
            filename, file_extension = os.path.splitext(fileone)
            print(filename, file_extension)
            if file_extension == '.JPEG':
                cls_select=PILImage
                print('JPEG')
            if file_extension == '.png':
                cls_select=PILImage
                print('png')
            if file_extension == '.jpg':
                cls_select=PILImage
                print('jpg')
            if file_extension == '.PNG':
                cls_select=PILImage
                print('PNG')
            if file_extension == '.dcm':
                cls_select=PILDicom
                print('dcm')
            else:
                print('format not found')
            bl = DataBlock(blocks=(ImageBlock(cls=PILImage), MaskBlock),
                        get_items = get_image_files,
                        get_y = get_msk,
                        item_tfms=Resize(224),
                        batch_tfms=[Normalize.from_stats(*imagenet_stats)]
                            )
            dls = bl.dataloaders(f'{dir}{train_fol}', bs=16)
            dls.show_batch()
    except FileNotFoundError:
        print('csv file not found')
    except AttributeError:
        print('column not found')
    except IndexError:
        print('check train folder')
    except TypeError:
        print('auto_block needs to have source and y_col(even if there is no csv file)')