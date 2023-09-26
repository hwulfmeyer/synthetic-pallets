import omni.replicator.core as rep

pallet_materials = [
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Wood/Laminate_Oak.mdl',
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Wood/OSB_Wood.mdl',
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Wood/OSB_Wood_Splattered.mdl',
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Wood/Wood_Cork.mdl',
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Paper/Cardboard_Low_Quality.mdl',
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Leather/Semi_Aniline_Leather.mdl',
    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Leather/Aniline_Leather.mdl',
    'omniverse://localhost/NVIDIA/Materials/Base/Wood/Mahogany.mdl',
    'omniverse://localhost/NVIDIA/Materials/Base/Wood/Timber.mdl',
    'omniverse://localhost/NVIDIA/Materials/Base/Wood/Walnut.mdl',
    'omniverse://localhost/NVIDIA/Materials/Base/Wood/Cherry.mdl',
    'omniverse://localhost/NVIDIA/Materials/Base/Wood/Oak.mdl',
    'omniverse://localhost/NVIDIA/Materials/Base/Wood/Plywood.mdl',
]

obj_materials = [
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Metal/Blued_Steel_Cold.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Metal/Copper_Antique_Brushed.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Metal/Titanium_Scratched.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Metal/Aluminum_Scratched.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Metal/Bronze_Hammered.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Metal/Iron_Scratched.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Masonry/Sandstone_Brick_Vintage.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Masonry/Facade_Brick_Red_Clinker.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Masonry/Facade_Brick_Grey.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/Concrete_Polished.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/Concrete_Wall_Aged_Scratched.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/Concrete_Rough.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/Stone_Pores_Weathered.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/Concrete_Precast.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/Mortar.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Stone/Steel_Grey.mdl',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Stone/Stone_Natural_Black.mdl',
                    ]

obj_materials += pallet_materials

with rep.new_layer():

    def dome_lights():
        lights = rep.create.light(
            light_type="Dome",
            rotation=rep.distribution.uniform((270, 0, 0), (270, 360, 0)),
            texture=rep.distribution.choice(
                [
                    "omniverse://localhost/NVIDIA/Assets/Skies/Indoor/autoshop_01_4k.hdr",
                    "omniverse://localhost/NVIDIA/Assets/Skies/Indoor/old_bus_depot_4k.hdr",
                    "omniverse://localhost/NVIDIA/Assets/Skies/Indoor/ZetoCG_com_WarehouseInterior2b.hdr",
                    "omniverse://localhost/NVIDIA/Assets/Skies/Indoor/ZetoCGcom_ExhibitionHall_Interior1.hdr",
                ]
            ),
            intensity=rep.distribution.normal(500, 200),
            temperature=rep.distribution.normal(6500, 1000)
        )
        return lights.node
    
    rep.randomizer.register(dome_lights)

    
    def sphere_lights(num):
        lights = rep.create.light(
            light_type="distant",
            temperature=rep.distribution.normal(6500, 500),
            intensity=rep.distribution.normal(400, 250),
            rotation=(-90,0,0),
            position=rep.distribution.uniform((-2000, 500, -2000), (2000, 500, 2000)),
            scale=rep.distribution.uniform(50, 100),
            count=num
        )
        return lights.node

    rep.randomizer.register(sphere_lights)

    # Define the path to the pallet USD file
    PALLET_USD = "omniverse://localhost/NVIDIA/Assets/ArchVis/Industrial/Pallets/Pallet_B1.usd"
    plane_x=500
    plane_y=700

    # Create randomizer function for pallet assets
    def env_pallets(size=None):
        pallets = rep.randomizer.instantiate(
            [PALLET_USD],  # Note: Here we use a list containing the USD path as the argument
            size=size,
            mode="reference",
        )
        with pallets:
            rep.modify.pose(
                position=rep.distribution.uniform((-plane_x, 0, -plane_y), (plane_x, 200, -100)),
                rotation=rep.distribution.uniform((-90, -180, 0), (-90, 180, 0)),
            )
            rep.randomizer.materials(pallet_materials)
            rep.modify.semantics([("class", "pallet")])

        return pallets.node

    #rep.randomizer.register(env_pallets)



    # Setup camera
    camera = rep.create.camera(focal_length=6)
    plane = rep.create.plane(scale=100, visible=True)
    cubes = rep.create.cube(count=3)
    cylinders = rep.create.cylinder(count=3)
    randomobjects = rep.create.group([cubes, cylinders])

    pallets_list = [rep.create.from_usd(PALLET_USD) for _ in range(41)]
    pallets_group = rep.create.group(pallets_list, semantics=[("class", "pallet")])

    # trigger on frame for an interval
    frames=600
    material_interval=10
    plane_interval=3

    with rep.trigger.on_frame(num_frames=int(frames*material_interval)):
                
        rep.randomizer.dome_lights()
        rep.randomizer.sphere_lights(4)
        #rep.randomizer.env_pallets(45)

        with pallets_group:
            rep.modify.pose(
                position=rep.distribution.uniform((-plane_x, 0, -plane_y), (plane_x, 200, -100)),
                rotation=rep.distribution.uniform((-90, -180, 0), (-90, 180, 0)),
            )

        with camera:
            rep.modify.pose(
                position=rep.distribution.uniform((0, 0, 50), (0, 150, 50)),
            )

        with randomobjects:
            rep.modify.pose(
                position=rep.distribution.uniform((-plane_x, 0, -plane_y/2), (plane_x, 0, -100)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
                scale=rep.distribution.uniform((1, 1, 1), (1.2, 10, 1.2)),
            )

    with rep.trigger.on_frame(num_frames=int(frames*material_interval/plane_interval), interval=plane_interval): 
        with plane:
            rep.randomizer.materials(materials=obj_materials)


    with rep.trigger.on_frame(num_frames=frames, interval=material_interval):
        with randomobjects:
            rep.randomizer.materials(materials=obj_materials)
        with pallets_group:
            rep.randomizer.materials(materials=pallet_materials)

    # Initialize and attach writer
    render_product = rep.create.render_product(camera, resolution=(1280, 1280))
    basic_writer = rep.WriterRegistry.get("BasicWriter")
    basic_writer.initialize(
        output_dir=f"replicator_pallets_random_2",
        rgb=True,
        bounding_box_2d_tight=True,
        bounding_box_3d=True,
        camera_params=True,
        distance_to_camera=True,
        frame_padding=5
    )
    basic_writer.attach([render_product])
        
    #rep.orchestrator.preview()
    #rep.orchestrator.run()