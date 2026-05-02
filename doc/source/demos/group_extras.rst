Extras
======

.. toctree::
	:hidden:
	:maxdepth: 1

	demo_2d_colorbar_in_canva
	demo_2d_colorbar_in_information
	demo_2d_draggable
	demo_2d_event

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
   </style>

   <div class="demo-grid">
     <div class="demo-card">
       <a href="demo_2d_colorbar_in_canva.html">
         <img src="../media/thumbnails/2d_colorbar_in_canva.png"
              onmouseover="this.src='../media/2d_colorbar_in_canva.gif'"
              onmouseout="this.src='../media/thumbnails/2d_colorbar_in_canva.png'">
         <div class="demo-card-title">Colorbar In Canva</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demo_2d_colorbar_in_information.html">
         <img src="../media/thumbnails/2d_colorbar_in_information.png"
              onmouseover="this.src='../media/2d_colorbar_in_information.gif'"
              onmouseout="this.src='../media/thumbnails/2d_colorbar_in_information.png'">
         <div class="demo-card-title">Colorbar In Information</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demo_2d_draggable.html">
         <img src="../media/thumbnails/2d_draggable.png"
              onmouseover="this.src='../media/2d_draggable.gif'"
              onmouseout="this.src='../media/thumbnails/2d_draggable.png'">
         <div class="demo-card-title">Draggable</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demo_2d_event.html">
         <img src="../media/thumbnails/2d_event.png"
              onmouseover="this.src='../media/2d_event.gif'"
              onmouseout="this.src='../media/thumbnails/2d_event.png'">
         <div class="demo-card-title">Event</div>
       </a>
     </div>
   </div>
