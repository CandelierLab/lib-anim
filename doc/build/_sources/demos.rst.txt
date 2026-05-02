Demos
=====

This page lists runnable examples showcasing key animation objects and update patterns.

.. toctree::
	:hidden:

	demos/group_structure
	demos/group_2d_items
	demos/group_extras

.. raw:: html

   <style>
   .demo-grid {
     display: grid;
     grid-template-columns: repeat(3, 1fr);
     gap: 16px;
     margin: 24px 0 40px 0;
   }
   .demo-card {
     background: #2a2d3a;
     border-radius: 8px;
     overflow: hidden;
     transition: background 0.2s;
   }
   .demo-card:hover { background: #1a2744; }
   .demo-card a {
     display: block;
     text-decoration: none;
     color: inherit;
     padding: 12px 12px 14px 12px;
   }
   .demo-card img {
     width: 100%;
     display: block;
     border-radius: 4px;
     object-fit: cover;
     aspect-ratio: 1 / 1;
   }
   .demo-card-title {
     margin-top: 10px;
     text-align: center;
     font-size: 0.9em;
     color: #ccc;
     font-weight: 500;
   }
   .demo-section-title {
     font-size: 1.2em;
     font-weight: 600;
     color: #aac4e8;
     margin: 32px 0 12px 0;
     border-bottom: 1px solid #3a3d4a;
     padding-bottom: 6px;
   }
   </style>

   <div class="demo-section-title">Structure</div>
   <div class="demo-grid">
     <div class="demo-card">
       <a href="demos/demo_informations.html">
         <img src="media/thumbnails/informations.png"
              onmouseover="this.src='media/informations.gif'"
              onmouseout="this.src='media/thumbnails/informations.png'">
         <div class="demo-card-title">Informations</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_multiple_canva.html">
         <img src="media/thumbnails/multiple_canva.png"
              onmouseover="this.src='media/multiple_canva.gif'"
              onmouseout="this.src='media/thumbnails/multiple_canva.png'">
         <div class="demo-card-title">Multiple Canva</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_grid.html">
         <img src="media/thumbnails/2d_grid.png"
              onmouseover="this.src='media/2d_grid.gif'"
              onmouseout="this.src='media/thumbnails/2d_grid.png'">
         <div class="demo-card-title">2D Grid</div>
       </a>
     </div>
   </div>

   <div class="demo-section-title">2D Items</div>
   <div class="demo-grid">
     <div class="demo-card">
       <a href="demos/demo_2d_line.html">
         <img src="media/thumbnails/2d_line.png"
              onmouseover="this.src='media/2d_line.gif'"
              onmouseout="this.src='media/thumbnails/2d_line.png'">
         <div class="demo-card-title">Line</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_path.html">
         <img src="media/thumbnails/2d_path.png"
              onmouseover="this.src='media/2d_path.gif'"
              onmouseout="this.src='media/thumbnails/2d_path.png'">
         <div class="demo-card-title">Path</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_circle.html">
         <img src="media/thumbnails/2d_circle.png"
              onmouseover="this.src='media/2d_circle.gif'"
              onmouseout="this.src='media/thumbnails/2d_circle.png'">
         <div class="demo-card-title">Circle</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_ellipse.html">
         <img src="media/thumbnails/2d_ellipse.png"
              onmouseover="this.src='media/2d_ellipse.gif'"
              onmouseout="this.src='media/thumbnails/2d_ellipse.png'">
         <div class="demo-card-title">Ellipse</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_rectangle.html">
         <img src="media/thumbnails/2d_rectangle.png"
              onmouseover="this.src='media/2d_rectangle.gif'"
              onmouseout="this.src='media/thumbnails/2d_rectangle.png'">
         <div class="demo-card-title">Rectangle</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_polygon.html">
         <img src="media/thumbnails/2d_polygon.png"
              onmouseover="this.src='media/2d_polygon.gif'"
              onmouseout="this.src='media/thumbnails/2d_polygon.png'">
         <div class="demo-card-title">Polygon</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_text.html">
         <img src="media/thumbnails/2d_text.png"
              onmouseover="this.src='media/2d_text.gif'"
              onmouseout="this.src='media/thumbnails/2d_text.png'">
         <div class="demo-card-title">Text</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_image_array.html">
         <img src="media/thumbnails/2d_image_array.png"
              onmouseover="this.src='media/2d_image_array.gif'"
              onmouseout="this.src='media/thumbnails/2d_image_array.png'">
         <div class="demo-card-title">Image Array</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_image_file.html">
         <img src="media/thumbnails/2d_image_file.png"
              onmouseover="this.src='media/2d_image_file.gif'"
              onmouseout="this.src='media/thumbnails/2d_image_file.png'">
         <div class="demo-card-title">Image File</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_arrow.html">
         <img src="media/thumbnails/2d_arrow.png"
              onmouseover="this.src='media/2d_arrow.gif'"
              onmouseout="this.src='media/thumbnails/2d_arrow.png'">
         <div class="demo-card-title">Arrow</div>
       </a>
     </div>
   </div>

   <div class="demo-section-title">Extras</div>
   <div class="demo-grid">
     <div class="demo-card">
       <a href="demos/demo_2d_colorbar_in_canva.html">
         <img src="media/thumbnails/2d_colorbar_in_canva.png"
              onmouseover="this.src='media/2d_colorbar_in_canva.gif'"
              onmouseout="this.src='media/thumbnails/2d_colorbar_in_canva.png'">
         <div class="demo-card-title">Colorbar In Canva</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_colorbar_in_information.html">
         <img src="media/thumbnails/2d_colorbar_in_information.png"
              onmouseover="this.src='media/2d_colorbar_in_information.gif'"
              onmouseout="this.src='media/thumbnails/2d_colorbar_in_information.png'">
         <div class="demo-card-title">Colorbar In Information</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_draggable.html">
         <img src="media/thumbnails/2d_draggable.png"
              onmouseover="this.src='media/2d_draggable.gif'"
              onmouseout="this.src='media/thumbnails/2d_draggable.png'">
         <div class="demo-card-title">Draggable</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demos/demo_2d_event.html">
         <img src="media/thumbnails/2d_event.png"
              onmouseover="this.src='media/2d_event.gif'"
              onmouseout="this.src='media/thumbnails/2d_event.png'">
         <div class="demo-card-title">Event</div>
       </a>
     </div>
   </div>


