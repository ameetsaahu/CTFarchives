var Snow = function(){

	var c = this;
	canvas = document.getElementById("snow");
	ctx = canvas.getContext("2d");

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
	W = canvas.width;
	H = canvas.height;

	this.init = function(){

		c.particles = [];
		c.colors = [
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
			'#ffffff',
		];
		

		c.mp = 100; //max particles

		for(var i = 0; i < c.mp; i++)
		{
			var size = Math.random()*4+5;
			c.particles.push({
				x: Math.random()*W, //x-coordinate
				y: Math.random()*H, //y-coordinate
				w: size,
				h: size,
				d: Math.random()*20 +30, //density
				vx:(Math.random()*7) - 3.5,
				fill: c.colors[Math.floor(Math.random() * c.colors.length)],
				s: (Math.random() * 0.2) - 0.1
			});
		}

    setInterval(function(){
      c.render();
    }, 1000/30);
    
	};

	this.resize = function(){
		// Nothing
	};

	//Lets draw the flakes
	this.render = function ()
	{
		ctx.fillStyle = '#000000';
		ctx.fillRect(0, 0, W, H);
		
		ctx.beginPath();
		for(var i = 0; i < c.mp; i++)
		{
			var p = c.particles[i];
			ctx.fillStyle = p.fill;
			ctx.fillRect(p.x, p.y, p.w, p.h);
		}
		ctx.fill();
		c.update_positions();
	};

	this.update_positions = function ()
	{
		for(var i = 0; i < c.mp; i++){
			var p = c.particles[i];
			p.a += p.s;
			p.y += p.d/10;
			p.x += p.vx;

			if(p.x > W+5 || p.x < -5 || p.y > H){
				if(i%3 > 0){
					p.x = Math.random()*W;
					p.y = -10;
				}
			}
		}
	};

	this.init();
};
