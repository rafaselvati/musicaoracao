"""Original synthesized ambient soundscapes. No samples, voices or therapeutic claims."""
from pathlib import Path
import numpy as np, subprocess, json
P=Path(__file__).resolve().parents[1];out=P/'private_files/audio';out.mkdir(exist_ok=True,parents=True)
tracks=[('01_Pausa_396Hz',396,'Pausa'),('02_Presencia_417Hz',417,'Presencia'),('03_Espacio_432Hz',432,'Espacio'),('04_Quietud_528Hz',528,'Quietud'),('05_Encuentro_639Hz',639,'Encuentro'),('06_Horizonte_741Hz',741,'Horizonte'),('07_Continuidad_852Hz',852,'Continuidad')]
sr=44100;duration=300;infos=[]
for idx,(slug,freq,title) in enumerate(tracks):
 command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','96k','-metadata','title='+title+' - '+str(freq)+' Hz','-metadata','artist=Séptimo Sentido','-metadata','album=Frecuencias de Contemplación','-metadata','comment=Ambiente sonoro original. Frecuencia central musical; sin afirmaciones terapéuticas.','-t',str(duration),str(out/(slug+'.mp3'))]
 process=subprocess.Popen(command,stdin=subprocess.PIPE)
 peak=0.;sq=0.;samples=0
 for second in range(duration):
  t=second+np.arange(sr)/sr
  fade=np.minimum(1,t/14)*np.minimum(1,(duration-t)/18);fade=np.clip(fade,0,1)
  # Soft continuous tones, slow amplitude envelopes, identical carrier pitch in both channels.
  carrier=.20*np.sin(2*np.pi*freq*t)*(.88+.12*np.cos(2*np.pi*t/43))
  low=.15*np.sin(2*np.pi*(freq/4)*t)*(.75+.25*np.sin(2*np.pi*t/59+.4))
  pad=.08*np.sin(2*np.pi*(freq/2)*t)+.04*np.sin(2*np.pi*(freq*.75)*t+.6)
  sparkle=.022*np.sin(2*np.pi*(freq*1.5)*t)*(.5+.5*np.sin(2*np.pi*t/31))
  middle=carrier+low+pad
  spread=.02*np.sin(2*np.pi*freq*1.25*t)*np.sin(2*np.pi*t/71)
  audio=np.stack([(middle+sparkle+spread)*fade,(middle+sparkle-spread)*fade],axis=1).astype('<f4')
  peak=max(peak,float(np.abs(audio).max()));sq+=float(np.square(audio).sum());samples+=audio.size
  process.stdin.write(audio.tobytes())
 process.stdin.close();assert process.wait()==0
 file=out/(slug+'.mp3');assert file.stat().st_size<4_400_000
 infos.append({'id':'audio'+str(idx+1),'file':'audio/'+file.name,'title':title,'frequency_hz':freq,'duration_seconds':duration,'size_bytes':file.stat().st_size,'source_peak':peak,'source_rms':(sq/samples)**.5})
 print(title, file.stat().st_size, 'bytes',flush=True)
(P/'content-tools/audio_manifest.json').write_text(json.dumps(infos,ensure_ascii=False,indent=2))
# A short, clearly labeled public listening sample, only 25 seconds of the 432 Hz track.
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','25','-i',str(out/'03_Espacio_432Hz.mp3'),'-t','25','-af','afade=t=in:d=2,afade=t=out:st=22:d=3','-c:a','libmp3lame','-b:a','96k',str(P/'assets/muestra-432hz.mp3')],check=True)
