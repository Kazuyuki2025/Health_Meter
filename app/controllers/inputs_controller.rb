class InputsController < ApplicationController
  def create
    uploaded_file = params[:video_file]

    if uploaded_file.nil?
      flash[:alert] = "ファイルを選択してください。"
      Rails.logger.info "Flash Alert: #{flash[:alert]}"
      redirect_to inputs_path
      return
    end

    # ファイルを保存
    save_path = Rails.root.join('public', 'video', uploaded_file.original_filename)
    FileUtils.mkdir_p(File.dirname(save_path))
    File.open(save_path, 'wb') { |file| file.write(uploaded_file.read) }

    # コーデックの判定，"H.264"出でない場合は変換
    movie = FFMPEG::Movie.new(save_path.to_s)
    puts "---------------\nMovie Codec: #{movie.video_codec}\n"
    if movie.video_codec != "h264"
      h264_path = save_path.to_s.sub(/\.mp4\z/, '_h264.mp4')
      movie.transcode(h264_path, %w(-vcodec libx264 -acodec aac -movflags +faststart))
      FileUtils.mv(h264_path, save_path) # 上書き
    end

    # パスをデータベースに保存
    video = Video.new(path: "video/#{uploaded_file.original_filename}")
    puts "\nVideo ID: #{flash[:video_id]}\n"
    if video.save
      flash[:video_id] = video.id
      flash[:notice] = "動画がアップロードされ、データベースに保存されました。"
      Rails.logger.info "Flash Notice: #{flash[:notice]}"

      # Pythonスクリプトを呼び出す
      script_path = Rails.root.join('app/controllers/python/detect_video.py')
      puts "\n1\n"
      output_image_path = Rails.root.join('public', 'output', "#{SecureRandom.hex(8)}.jpg")
      puts "\n2\n"
      video_path = save_path.to_s
      puts "\n3\n"

      result = `python3 #{script_path} #{video_path} #{output_image_path}`
      puts "\n4\n"
      puts "Python script output: #{result}"

      # JSON形式でPythonから返されたデータを処理
      begin
        #bounding_boxes = JSON.parse(result.match(/Bounding Box Data: (.+)/)[0])
        flash[:notice] += "YOLO解析が完了しました。画像を確認してください。".html_safe
        puts "\n5\n"
        @output_image_url = "/output/#{File.basename(output_image_path)}"
        flash[:output_image_url] = @output_image_url
        #puts "\n@output_image_url: #{@output_image_url}\n"
      rescue JSON::ParserError => e
        flash[:alert] = "解析結果の読み込みに失敗しました: #{e.message}"
        puts "\n6\n"
        Rails.logger.error "Flash Alert: #{flash[:alert]}"
      end
    else
      flash[:alert] = "動画のアップロードに成功しましたが、データベースへの保存に失敗しました。"
      puts "\n7\n" 
      Rails.logger.error "Flash Alert: #{flash[:alert]}"
    end

    redirect_to inputs_path
  rescue => e
    flash[:alert] = "動画のアップロード中にエラーが発生しました: #{e.message}"
    puts "\n8\n"
    Rails.logger.error "Flash Alert: #{flash[:alert]}"
    redirect_to inputs_path
  end
end
