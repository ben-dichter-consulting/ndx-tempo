from pynwb.spec import NWBDatasetSpec, NWBNamespaceBuilder, \
    NWBGroupSpec, NWBAttributeSpec, NWBDtypeSpec, NWBLinkSpec
from export_spec import export_spec
name = 'ndx-tempo'
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"


def main():
    ns_builder = NWBNamespaceBuilder(
        doc='nwb extention for voltage imaging technique called TEMPO',
        name=name,
        version='0.1.0',
        author=list(map(str.strip, 'Saksham Sharda'.split(','))),
        contact=list(map(str.strip, 'sxs1790@case.edu'.split(',')))
    )

    ns_builder.include_type('VectorData', namespace='hdmf-common')
    ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('Device', namespace='core')

    measurement = NWBDatasetSpec('Flexible vectordataset with a custom unit/conversion/resolution'
                                 ' field similar to timeseries.data',
                                 attributes=[
                                     NWBAttributeSpec('unit',
                                                      'The base unit of measure used to store data. This should be in the SI unit.'
                                                      'COMMENT: This is the SI unit (when appropriate) of the stored data, such as '
                                                      'Volts. If the actual data is stored in millivolts, the field ''conversion'' '
                                                      'below describes how to convert the data to the specified SI unit.',
                                                      'text'),
                                     NWBAttributeSpec('conversion',
                                                      'Scalar to multiply each element in '
                                                      'data to convert it to the specified unit',
                                                      'float32', required=False, default_value=1.0),
                                     NWBAttributeSpec('resolution',
                                                      'Smallest meaningful difference between values in data, stored in the specified '
                                                      'by unit. COMMENT: E.g., the change in value of the least significant bit, or '
                                                      'a larger number if signal noise is known to be present. If unknown, use -1.0',
                                                      'float32', required=False, default_value=0.0)
                                 ],
                                 neurodata_type_def='Measurement',
                                 neurodata_type_inc='VectorData',
                                 )

    # Typedef for laserline
    laserline_device = NWBGroupSpec(neurodata_type_def='LaserLine',
                                    neurodata_type_inc='Device',
                                    doc='description of laserline device, part for a TEMPO device',
                                    attributes=[
                                        NWBAttributeSpec('reference',
                                                         'reference of the laserline module',
                                                         dtype='text',
                                                         required=False)
                                    ],
                                    quantity='*')

    laserline_device.add_dataset(
        name='analog_modulation_frequency',
        neurodata_type_inc=measurement,
        doc='analog_modulation_frequency of the laserline module',
        shape=(1,),
        dtype='text',
        quantity='?'
    )

    laserline_device.add_dataset(
        name='power',
        neurodata_type_inc=measurement,
        doc='power of the laserline module',
        shape=(1,),
        dtype='float',
        quantity='?'
    )

    laserline_devices = NWBGroupSpec(neurodata_type_def='LaserLineDevices',
                                     neurodata_type_inc='NWBDataInterface',
                                     name='laserline_devices',
                                     doc='A container for dynamic addition of LaserLine devices',
                                     quantity='?',
                                     groups=[laserline_device])

    # Typedef for PhotoDetector
    photodetector_device = NWBGroupSpec(neurodata_type_def='PhotoDetector',
                                        neurodata_type_inc='Device',
                                        doc='description of photodetector device, part for a TEMPO device',
                                        attributes=[
                                            NWBAttributeSpec('reference',
                                                             'reference of the photodetector module',
                                                             dtype='text',
                                                             required=False)
                                        ],
                                        quantity='*')

    photodetector_device.add_dataset(
        name='gain',
        neurodata_type_inc=measurement,
        doc='gain of the photodetector module',
        shape=(1,),
        dtype='float',
        quantity='?'
    )

    photodetector_device.add_dataset(
        name='bandwidth',
        neurodata_type_inc=measurement,
        doc='bandwidth metadata of the photodetector module',
        shape=(1,),
        dtype='float',
        quantity='?'
    )

    photodetector_devices = NWBGroupSpec(neurodata_type_def='PhotoDetectorDevices',
                                         neurodata_type_inc='NWBDataInterface',
                                         name='photodetector_devices',
                                         doc='A container for dynamic addition of PhotoDetector devices',
                                         quantity='?',
                                         groups=[photodetector_device])

    # Typedef for LockInAmplifier
    lockinamp_device = NWBGroupSpec(neurodata_type_def='LockInAmplifier',
                                    neurodata_type_inc='DynamicTable',
                                    doc='description of lock_in_amp device, part for a TEMPO device',
                                    attributes=[
                                        NWBAttributeSpec('demodulation_filter_order',
                                                         'demodulation_filter_order of the lockinamp_device module',
                                                         dtype='float',
                                                         required=False,
                                                         default_value=-1),
                                        NWBAttributeSpec('reference',
                                                         'reference of the lockinamp_device module',
                                                         dtype='text',
                                                         required=False)
                                    ],
                                    quantity='*')

    lockinamp_device.add_dataset(
        name='demod_bandwidth',
        neurodata_type_inc=measurement,
        doc='demod_bandwidth of lock_in_amp',
        shape=(1,),
        dtype='float',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='channel_name',
        neurodata_type_inc='VectorData',
        doc='name of the channel of lock_in_amp',
        dims=('no_of_channels',),
        shape=(None,),
        dtype='text',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='offset',
        neurodata_type_inc=measurement,
        doc='offset for channel of lock_in_amp',
        dims=('no_of_channels',),
        shape=(None,),
        dtype='float',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='gain',
        neurodata_type_inc='VectorData',
        doc='gain for channel of lock_in_amp',
        dims=('no_of_channels',),
        shape=(None,),
        dtype='float',
        quantity='?'
    )

    lockinamp_devices = NWBGroupSpec(neurodata_type_def='LockInAmplifierDevices',
                                     neurodata_type_inc='NWBDataInterface',
                                     name='lockinamp_devices',
                                     doc='A container for dynamic addition of LockInAmplifier devices',
                                     quantity='?',
                                     groups=[lockinamp_device])

    tempo_device = NWBGroupSpec(neurodata_type_def='TEMPO',
                                neurodata_type_inc='Device',
                                doc='datatype for a TEMPO device',
                                attributes=[NWBAttributeSpec(
                                    name='no_of_modules',
                                    doc='the number of electronic modules with this acquisition system',
                                    dtype='int',
                                    required=False,
                                    default_value=3)],
                                groups=[laserline_devices,
                                        photodetector_devices,
                                        lockinamp_devices]
                                )

    # surgical meta-data specification:

    surgery = NWBGroupSpec(neurodata_type_def='Surgery',
                           neurodata_type_inc='Subject',
                           doc='Surgery related meta-data of subject',
                           name='surgery_data',
                           attributes=[NWBAttributeSpec(
                                   name='surgery_date',
                                   doc='date of surgery',
                                   dtype='text',
                                   required=False),
                               NWBAttributeSpec(
                                   name='surgery_notes',
                                   doc='surgery notes',
                                   dtype='text',
                                   required=False),
                               NWBAttributeSpec(
                                   name='surgery_pharmacology',
                                   doc='pharmacology data',
                                   dtype='text',
                                   required=False),
                               NWBAttributeSpec(
                                   name='surgery_arget_anatomy',
                                   doc='target anatomy of the surgery',
                                   dtype='text',
                                   required=False)],
                           groups=[
                                NWBGroupSpec(
                                   name='implantation',
                                   doc='implantation related data',
                                   links=[NWBLinkSpec(name='implantation_device',
                                                      doc='device implanted during surgery',
                                                      target_type='Device')],
                                   attributes=[NWBAttributeSpec(
                                                  name='ophys_implant_name',
                                                  doc='optical physiology implant name',
                                                  dtype='text',
                                                  required=False),
                                               NWBAttributeSpec(
                                                 name='ephys_implant_name',
                                                 doc='electrophysiology implant name',
                                                 dtype='text',
                                                 required=False)],
                                   quantity='?'),
                                NWBGroupSpec(
                                    name='virus_injection',
                                    doc='virus injection related data',
                                    attributes=[NWBAttributeSpec(
                                                   name='virus_injection_id',
                                                   doc='id of virus injected',
                                                   dtype='text',
                                                   required=False),
                                                NWBAttributeSpec(
                                                    name='virus_injection_opsin',
                                                    doc='opsin/protein used',
                                                    dtype='text',
                                                    required=False),
                                                NWBAttributeSpec(
                                                    name='virus_injection_opsin_l_r',
                                                    doc='opsin/protein left/right description'
                                                        'enter \'L\' or \'R\'',
                                                    dtype='text',
                                                    required=False,
                                                    default_value='L/R'),
                                                NWBAttributeSpec(
                                                    name='virus_injection_scheme',
                                                    doc='description of injection scheme eg.'
                                                    '\'single_bolus\'',
                                                    dtype='text',
                                                    required=False),
                                                NWBAttributeSpec(
                                                    name='virus_injection_tag',
                                                    doc='tag for the virus injected',
                                                    dtype='text',
                                                    required=False),
                                                NWBAttributeSpec(
                                                    name='virus_injection_coordinates_description',
                                                    doc='description of coordinates'
                                                        '\'AP\'/\'ML\'/\'DV\'',
                                                    dtype='text',
                                                    required=False),
                                                NWBAttributeSpec(
                                                    name='virus_injection_volume',
                                                    doc='volume of virus injected in ml',
                                                    dtype='float',
                                                    required=False,
                                                    default_value=-1.0)],
                                    datasets=[NWBDatasetSpec(
                                                    name='virus_injection_coordinates',
                                                    doc='coordinates of virus injection',
                                                    dtype='text',
                                                    quantity='?')],
                                    quantity='?'),
                                NWBGroupSpec(
                                    name='ophys_injection',
                                    doc='optical physiology fluorescence injection metadata',
                                    attributes=[NWBAttributeSpec(
                                                    name='ophys_injection_date',
                                                    doc='date of fluorscent protein injection',
                                                    dtype='text',
                                                    required=False),
                                                NWBAttributeSpec(
                                                    name='ophys_injection_volume',
                                                    doc='volume of fluorscent protein injected',
                                                    dtype='float',
                                                    required=False),
                                                NWBAttributeSpec(
                                                    name='ophys_injection_brain_area',
                                                    doc='brain area of fluorscent protein injection',
                                                    dtype='text',
                                                    required=False)
                                                ],
                                    datasets=[NWBDatasetSpec(
                                                    name='ophys_injection_flr_protein_data',
                                                    doc='fluorescence protein name and concentration table',
                                                    neurodata_type_inc='DynamicTable')
                                              ],
                                    quantity='?')
                                    ],
                           quantity='?')

    subject = NWBGroupSpec(
                        neurodata_type_def='SubjectComplete',
                        neurodata_type_inc='Surgery',
                        doc='Mouse metadata used with the TEMPO device',
                        attributes=[NWBAttributeSpec(
                                       name='sacrificial_date',
                                       doc='sacrificial date of the animal ',
                                       dtype='text',
                                       required=False),
                                    NWBAttributeSpec(
                                       name='strain',
                                       doc='strain of the animal',
                                       dtype='text',
                                       required=False)],
                           )

    new_data_types = [measurement, tempo_device, surgery, subject]
    export_spec(ns_builder, new_data_types)


if __name__ == "__main__":
    main()
