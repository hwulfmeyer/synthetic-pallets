import omni.replicator.core as rep

#.\omni.code.bat --no-window --/omni/replicator/script=D:\code\synthetic-pallets\create_scene.py

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

all_materials = obj_materials+pallet_materials

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
            intensity=rep.distribution.normal(300, 200),
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
            position=rep.distribution.uniform((-2000, 1000, -2000), (2000, 1000, 2000)),
            scale=rep.distribution.uniform(50, 100),
            count=num
        )
        return lights.node

    rep.randomizer.register(sphere_lights)

    # Define the path to the pallet USD file
    PALLET_USD = "omniverse://localhost/NVIDIA/Assets/ArchVis/Industrial/Pallets/Pallet_B1.usd"
    plane_x=800
    plane_y=1200

    # Setup camera
    camera = rep.create.camera(focal_length=6)
    plane = rep.create.plane(scale=100, visible=True)

    pallets_leftside = [rep.create.from_usd(PALLET_USD) for _ in range(5)]
    pallets_leftside_group = rep.create.group(pallets_leftside, semantics=[("class", "pallet")])

    pallets_rightside = [rep.create.from_usd(PALLET_USD) for _ in range(5)]
    pallets_rightside_group = rep.create.group(pallets_rightside, semantics=[("class", "pallet")])

    pallets_all = rep.create.group(pallets_leftside+pallets_rightside, semantics=[("class", "pallet")])

    # trigger on frame for an interval
    frames=100
    material_interval=10
    plane_interval=3

    with rep.trigger.on_frame(num_frames=int(frames*material_interval)):
                
        rep.randomizer.dome_lights()
        rep.randomizer.sphere_lights(2)

        with pallets_leftside_group:
            rep.modify.pose(
                position=rep.distribution.uniform((-400, 0, -plane_y), (-400, 0, -300)),
                rotation=rep.distribution.choice([(-90, 0, 0), (-90, 0, 0)]),
            )

        with pallets_rightside_group:
            rep.modify.pose(
                position=rep.distribution.uniform((400, 0, -plane_y), (400, 0, -300)),
                rotation=rep.distribution.choice([(-90, 0, 0), (-90, 0, 0)]),
            )

        with camera:
            rep.modify.pose(
                position=rep.distribution.uniform((0, 20, 0), (0, 80, 0)),
                rotation=rep.distribution.normal((0, 0, 0), (0, 10, 0)),
            )

    with rep.trigger.on_frame(num_frames=int(frames*material_interval/plane_interval), interval=plane_interval): 
        with plane:
            rep.randomizer.materials(materials=obj_materials)


    with rep.trigger.on_frame(num_frames=frames, interval=material_interval):
        with pallets_all:
            rep.randomizer.materials(materials=pallet_materials)

    # Initialize and attach writer
    render_product = rep.create.render_product(camera, resolution=(1280, 1280))
    basic_writer = rep.WriterRegistry.get("BasicWriter")
    basic_writer.initialize(
        output_dir=f"pallets_side",
        rgb=True,
        bounding_box_2d_tight=True,
        bounding_box_3d=False,
        camera_params=False,
        distance_to_camera=False,
        frame_padding=5
    )
    basic_writer.attach([render_product])
        
    rep.orchestrator.preview()
    #rep.orchestrator.run()