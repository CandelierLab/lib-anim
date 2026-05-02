Structure
=========

.. toctree::
	:hidden:
	:maxdepth: 1

	demo_informations
	demo_multiple_canva
	demo_2d_grid

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
       <a href="demo_informations.html">
         <img src="../media/thumbnails/informations.png"
              onmouseover="this.src='../media/informations.gif'"
              onmouseout="this.src='../media/thumbnails/informations.png'">
         <div class="demo-card-title">Informations</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demo_multiple_canva.html">
         <img src="../media/thumbnails/multiple_canva.png"
              onmouseover="this.src='../media/multiple_canva.gif'"
              onmouseout="this.src='../media/thumbnails/multiple_canva.png'">
         <div class="demo-card-title">Multiple Canva</div>
       </a>
     </div>
     <div class="demo-card">
       <a href="demo_2d_grid.html">
         <img src="../media/thumbnails/2d_grid.png"
              onmouseover="this.src='../media/2d_grid.gif'"
              onmouseout="this.src='../media/thumbnails/2d_grid.png'">
         <div class="demo-card-title">2D Grid</div>
       </a>
     </div>
   </div>
