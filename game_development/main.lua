WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243 
PADDLE_SPEED = 200
Class = require 'class'
push = require 'push'
require 'Ball'
require 'Paddle'

function love.load()
    math.randomseed(os.time())
    love.graphics.setDefaultFilter('nearest', 'nearest')
    love.window.setTitle('Pong')
    smallFont = love.graphics.newFont('font.TTF', 8) 
    scoreFont = love.graphics.newFont('font.TTF', 32)
    victoryFont = love.graphics.newFont('font.TTF', 24)
    sounds = {
        ['paddle_hit'] = love.audio.newSource('paddle_hit.wav','static'),
        ['point_scored'] = love.audio.newSource('point_scored.wav','static'),
        ['wall_hit'] = love.audio.newSource('wall_hit.wav', 'static'),
        ['win_sound'] = love.audio.newSource('win.wav', 'static')
    }
    
    player1Score = 0
    player2Score = 0

    paddle1 = Paddle(5,20,5,20)
    paddle2 = Paddle(VIRTUAL_WIDTH-10, VIRTUAL_HEIGHT-30,5,20)
    ball = Ball(VIRTUAL_WIDTH/2-2, VIRTUAL_HEIGHT/2-2,4,4)
    servingPlayer = math.random(2) == 1 and 1 or 2
    winningPlayer = 0
    if servingPlayer == 1 then
        ball.dx = 100
    else
        ball.dx = -100
    end 

    gameState = 'start'
    love.graphics.setFont(smallFont) 
    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT,WINDOW_WIDTH,WINDOW_HEIGHT, {
        fullscreen = false,
        vsync = true,
        resizable = true
    })
end

function love.resize(w,h)
    push:resize(w,h)
end

function love.update(dt)
    if gameState == 'play' then 
        if ball.x <= 0 then 
            player2Score = player2Score+1
            servingPlayer = 1
            ball:reset()
            ball.dx = 100
            sounds['point_scored']:play()
            if player2Score >= 10 then
                gameState = 'victory'
                winningPlayer = 2
                sounds['win_sound']:play()
            else
                gameState = 'serve'
            end
        end
        if ball.x >= VIRTUAL_WIDTH - 4 then 
            player1Score = player1Score+1
            servingPlayer = 2
            ball:reset()
            ball.dx = -100
            sounds['point_scored']:play()
            if player1Score >= 10 then
                gameState = 'victory'
                winningPlayer = 1
                sounds['win_sound']:play()
            else
                gameState = 'serve'
            end      
        end
    
        if ball:collides(paddle1) then
            ball.dx = -ball.dx 
            ball.dy = math.random(-50, 50)
            sounds['paddle_hit']:play()
        end
        if ball:collides(paddle2) then
            ball.dx = -ball.dx
            ball.dy = math.random(-50, 50)
            sounds['paddle_hit']:play()
        end
        if ball.y <= 0 then 
            ball.dy = -ball.dy
            ball.y = 0
            sounds['wall_hit']:play()
        end
        if ball.y >= VIRTUAL_HEIGHT-4 then
            ball.dy = -ball.dy
            ball.y = VIRTUAL_HEIGHT-4
            sounds['wall_hit']:play()
        end
    end
    
    if love.keyboard.isDown('w') then
        paddle1.dy = -PADDLE_SPEED
    elseif love.keyboard.isDown('s') then 
        paddle1.dy = PADDLE_SPEED
    else
        paddle1.dy = 0
    end
    paddle1:update(dt)

    if gameState == 'play' then 
        ball:update(dt)
        if paddle2.y + paddle2.height/2 >= ball.y + ball.height and ball.dx >= 0 and ball.x > VIRTUAL_WIDTH/2 + 50 then 
            paddle2.dy = -95
        elseif paddle2.y + paddle2.height/2 <= ball.y and ball.dx > 0 and ball.x > VIRTUAL_WIDTH/2 + 50 then 
            paddle2.dy = 95
        elseif ball.x >= VIRTUAL_WIDTH and ball.dx > 0 then
            paddle2.dy = 0
        elseif ball.x < paddle2.x + paddle2.width and ball.x + ball.width > paddle2.x and ball.dx >0 then 
            paddle2.dy = 20
        else
            paddle2.dy = 0
        end
    end
    paddle2:update(dt)
end


function love.keypressed(key)

    if key == 'escape' then 
        love.event.quit()
    elseif key == 'enter' or key == 'return' then
        if gameState == 'start' then
            gameState = 'serve'
        elseif gameState == 'victory' then 
            gameState = 'start'
            player1Score = 0
            player2Score = 0
        elseif gameState == 'serve' then
            gameState = 'play'
        end
    end
end


function love.draw()
    push:apply('start')
-- change the background of the screen into dark green 
    love.graphics.clear(40/255, 45/255, 52/255, 1)
    love.graphics.setFont(smallFont)
    if gameState == 'start' then 
        love.graphics.printf("Welcome to Pong!", 0, 20, VIRTUAL_WIDTH,'center')
        love.graphics.printf("Press Enter to Play!", 0, 32, VIRTUAL_WIDTH, 'center')
    elseif gameState == 'serve' then
        love.graphics.printf("Player".. tostring(servingPlayer).."'s turn!", 0, 20, VIRTUAL_WIDTH,'center')
        love.graphics.printf("Press Enter to Serve!", 0, 32, VIRTUAL_WIDTH, 'center')
    elseif gameState == 'victory' then
        love.graphics.setFont(victoryFont)
        love.graphics.printf("Player".. tostring(winningPlayer).."wins!", 0, 10, VIRTUAL_WIDTH,'center')
        love.graphics.setFont(smallFont)
        love.graphics.printf("Press Enter to Play!", 0, 42, VIRTUAL_WIDTH, 'center')
    end 
-- draw the score 
    love.graphics.setFont(scoreFont)
    love.graphics.print(player1Score, VIRTUAL_WIDTH/2 -50,VIRTUAL_HEIGHT/3)
    love.graphics.print(player2Score, VIRTUAL_WIDTH/2 +30,VIRTUAL_HEIGHT/3)
-- draw the rectangle ball
    ball:render()
--draw the bars
    paddle1:render()
    paddle2:render()
    displayFPS()
    push:apply('end')
end

function displayFPS()
    love.graphics.setColor(0,1,0,1)
    love.graphics.setFont(smallFont)
    love.graphics.print('FPS: '..tostring(love.timer.getFPS()),40,20)
    love.graphics.setColor(1,1,1,1)

end
