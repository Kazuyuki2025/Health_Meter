class UnhealthyController < ApplicationController
  def index
    @performers = Performer.all.map do |performer|
      stats = performer.calculate_statistics
      next unless stats
      {
        id: performer.id,
        name: performer.name,
        latest_performance_date: stats[:latest_performance_date],
        low_z_count: stats[:low_z_count],
      }
    end.compact
    @performers.sort_by! { |performer| -performer[:low_z_count] }
  end

  def show
    performer = Performer.find(params[:id])
    stats = performer.calculate_statistics
    @performer_name = performer.name
    @latest_date = stats[:latest_performance_date]
    @problematic_activities = stats[:z_scores].select { |z| z[:z_score] <= -2.0 }.map do |z|
      {
        type: z[:category],
        z_score: z[:z_score].round(2)
      }
    end
    latest_performance = performer.performances.order(date: :desc).first
    puts "\nLatest Performance: #{latest_performance.inspect}\n"
    if latest_performance&.video
      @video_path = unhealthy_video_path(filename: File.basename(latest_performance.video.path, '.*'))
      puts "\nVideo Path: #{@video_path}\n"
    else
      @video_path = nil
    end
    @activity_types = {
      1 => "伸びの運動",
      2 => "腕を振って脚を曲げ伸ばす運動",
      3 => "腕を回す運動",
      4 => "胸を反らす運動",
      5 => "体を横に曲げる運動",
      6 => "体を前後に曲げる運動",
      7 => "体をねじる運動",
      8 => "腕を上下に伸ばす運動",
      9 => "体を斜め下に曲げ胸を反らす運動",
      10 => "体を回す運動",
      11 => "両脚で跳ぶ運動",
      12 => "腕を振って脚を曲げ伸ばす運動",
      13 => "深呼吸"
    }
  end

  def video
    filename = params[:filename]
    video_path = Rails.root.join('public', 'video', "#{filename}.mp4")
    puts "---------------\nVideo Path: #{video_path}\n"
    if File.exist?(video_path)
      puts "---------------\nVideo file exists: #{video_path}\n"
      send_file video_path, type: 'video/mp4', disposition: 'inline'
    else
      render plain: '動画が見つかりませんでした', status: :not_found
    end
  end
end
